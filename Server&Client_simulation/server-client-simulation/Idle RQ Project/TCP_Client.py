#
# TCP Client
#
from socket import *
from array import *
import packet
import Gremlin

lossProb = 0.02                          # prob of losing a packet
corruptProb =0.015                       # prob of corrupting a packet

def parseData(data): # code wasnt able t handle this in packet file? why?
    # --- tidying up the data --- #
    data = data.replace("b\"", "")
    data = data.replace("b\"", "")
    data = data.replace("\"", "")
    data = data.replace("\"", "")
    data = data.replace("--", "-")
    #print"Data is now: ", data
    pieces = data.split("-")
    return pieces


# DEFINE THE SOCKETS
serverName = "localhost"
serverPort = 12000
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except socket.error:
    print"Failed to create socket"
    exit(2)
print"Socket created successfully"
clientSocket.connect((serverName, serverPort))
print "Connection established to server"

file = open("TestData.txt", "rb")                       # open for reading and writing
data = file.read(12000)
fileremaining = len(data)                             # how much data in file left to send - counter
seq = 0                                               # seq num of the frame                                        # ack seq num
ack=False
ack_bits = 0
drop = False
corrupt = False
frame_size = 5

while fileremaining > 0:                              # while we still have something to send
    for chunk in packet.chunks(data, 8):                     # 8 bytes at a time of input data
        fileremaining -= len(chunk)                   # note chunk is in bytes

        # --- create the packet --- #
        print"------------------------------------------\n"
        print"Generating packet ", seq
        packetToSend = packet.packet(chunk, seq, "00")       # make the packet, complete with header and trailer
        problem = Gremlin.gremlin(packetToSend, corruptProb, lossProb)
        #print"Packet to send is \n", packet

        # --- error checks --- #
        if problem == "01":                            # packed was dropped
           print"Dropped packet"            # do not send the packet
           drop = True

        elif problem == "10":                          # corrupt packet
            print"Corrupted packet"
            corrupt = True
            #send corrupted packet - server deals with


        if drop == False:
            # it hasn"t been dropped - we can send it (don"t have to worry about it being corrupt on this side)
            # we can send it now - worry about if corrupted later
            if corrupt == True:
                clientSocket.send(bytes(corrupt_packet(packetToSend, seq)))           # send a corrupt packer
            else:
                clientSocket.send(bytes(packetToSend))                           # send a normal packet
            print"Sent"
            print"Waiting for acknowledgement from the server..\n"
            while ack != True:                         # we haven"t got an ack frame back
                acknowledgement = clientSocket.recv(32)
                # --- tidying up data --- #
                pieces = parseData(acknowledgement)
                print "peices = ", pieces
             
                flag = pieces[0]
                #  print"Flag is: ", flag
                ack_seq = pieces[1]
                print"seq: ", ack_seq
                ack_bits = pieces[2]
                # print"ack bits is: ", ack_bits
                payload = pieces[3]
                print"payload is: ", payload
                crc_recvd = pieces[4]
                
                if ack_bits == "10":                   # if an ACK
                    ack = True                         # we can move onto next chunk
                    print"Received ACK frame from server - packet ", seq, " sent successfully.\n"
                else:
                    # nack or ERROR ("00", "01", "11") received
                    print"Resent packet, received ack field=", ack_bits
                    clientSocket.send(bytes(packetToSend))                # resend the packet
            seq+=1                                    # lets go onto next frame
            print"Our next frame will be ", seq
            ack = False                                     # reset
            
        elif drop == True:
             packetToSend = packet.packet(chunk, seq, "00") # packet with wrong seq
             clientSocket.send(bytes(packetToSend))
             print"Sending incorrect packet, ", packetToSend
             print"Sent"
             print"Waiting for acknowledgement from the server.."
             while ack != True:                         # we haven"t got an ack frame back
                acknowledgement = clientSocket.recv(32)
                # --- tidying up data --- #
                pieces = parseData(str(acknowledgement))
                print"This is our new data (dropped packet last time)"
                
                flag = pieces[0]
                #  print"Flag is: ", flag
                ack_seq = pieces[1]
                print"seq: ", ack_seq
                ack_bits = pieces[2]
                # print"ack bits is: ", ack_bits
                payload = pieces[3]
                print"payload is: ", payload
                crc_recvd = pieces[4]

                if ack_bits == "10":                   # if an ACK
                    ack = True                         # we can move onto next chunk
                    print"Received ACK frame from server - packet ", seq, " sent successfully."
                else:
                    # nack or ERROR ("00", "01", "11") received
                    print"Just resent the packet - the original packet was dropped"
                    packetToSend = packet.packet(chunk, seq, "00")
                    clientSocket.send(bytes(packetToSend))                # resend the packet
             seq+=1                                    # lets go onto next frame
             print"Our next frame will be ", seq
             ack = False
        drop = False
        corrupt = False

    print"Stopped generating frames - end of file"
# only fall out of this loop if the amount of file remaining is 0
print"Sending completed"
file.close()
clientSocket.close()

