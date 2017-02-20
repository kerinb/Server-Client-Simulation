#
# TCP Server
#

from socket import *
import sys
import CRC
import packet
# ------- set up our sockets ------- #

def parseData(data):
    # --- tidying up the data --- #
    data = data.replace("b\'", "")
    data = data.replace("b\"", "")
    data = data.replace("\"", "")
    data = data.replace("\'", "")
    data = data.replace("--", "-")
    #print"Data is now: ", data
    pieces = data.split("-")
    return pieces

buf = 1500                                         # buffering size
serverPort = 12000
HOST = ''
try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
except socket.error:
    print"Failed to create socket"
    exit(2)
#print"Socket created successfully"
serverSocket.bind((HOST, 12000))
serverSocket.listen(1)                                      # starts listening - sets maximum accept rate to 1
print"The server is ready to receive"

correct_seq=0             # identify whether the sequence number received is the EXPECTED seq num
isValid=True               # checks whether the package received has any errors
frame_size = 5             # the num of frames we can receive at a time

# ---- deal with received data ---- #
file = open("output_text.txt", "wb")                         # open file for writing
connectionSocket, addr = serverSocket.accept()             # connected to client

while 1:
    print"Waiting for data"                           # connected to clien
    data = connectionSocket.recv(50000)                       # buffered data size
    data = str(data)
    print"Data is ", data
    # ---- tidy up the data ---- #
    pieces = parseData(data)
    flag = pieces[0]
  #  print"Flag is: ", flag
    ack_seq = pieces[1]
    print"seq: ", int(ack_seq)
    ack_bits = pieces[2]
   # print"ack bits is: ", ack_bits
    payload = pieces[3]
    print"payload is: ", payload
    crc_recvd = pieces[4]
    #print"crc received is: ", crc_recvd

    # ---- start checking for errors ---- #
    if ("101010101010" in data) == False:
        # not corrupted
        isValid = True                                      # valid for the moment - not corrupted

        print"Expected sequence number is ", correct_seq, ", got sequence number ", int(ack_seq)
        # -- start error-checking the data -- #
        if correct_seq != int(ack_seq):                              # error has occurred - send a nack to request retransmission
            isValid = False
            print"Incorrect sequence number - the original packet was dropped"
            dropped = True
            nack_packet = packet.packet(bytes(payload), correct_seq, "01")
            connectionSocket.send(bytes(nack_packet))                         # NACK
        else:                                                   # we have the correct sequence num - continue error-checking
           print"Correct sequence number"
        #    print"CRC received: ", crc_recvd
           chk = CRC.calc_checksum(bytes(payload))
           if chk != crc_recvd:
                isValid = False                                 # request a resend
                print"CRC fields do not match"
           else:
                isValid = True
                print"CRC correct"
    else:
        # packet corrupt
        print"Corrupt packet!"
        isValid = False

    if isValid == True:                                     # no errors - ACK frame
        ack_packet = packet.packet(bytes(payload), correct_seq, '10')
        connectionSocket.send(bytes(ack_packet))
        print"Sent the ack frame (",ack_packet ," ) for seq ", correct_seq, " back to the client"
        file.write(bytes(payload))                                   # write the data to the file once we know received correctly
        print"Wrote to the file"
        correct_seq+=1                                      # only increment the seq if the frame was 100% ok
    elif (isValid == False):           # we had errors
        print"Did not receive correct info from client - sent back a nack frame"
        nack_packet = packet.packet(bytes(payload), correct_seq, "01")
        connectionSocket.send(bytes(nack_packet))                         # NACK
    data = ""                                               # reset and continue listening for next packet


# only close the socket when we fall out of the loop
file.close()                                                # finished writing to file
connectionSocket.close()
