#
# Breandan Kerin
# 14310166
# TCP Client
#
from socket import *
import os, sys
from binascii import hexlify
from struct import *
import binascii

# -------- Defining The Sockets -------- #
serverName = 'localhost'
serverPort = 12000
try:                                                    #Try and connect to socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
except socket.error:                                    # Connecetiuon failed
    print("Socket Failed To Be Created")
    exit(1)

print("Socket Created Successfully")
clientSocket.connect((serverName,serverPort))
print("Connection Established To Server")

#------Funstions Used------#     
def chunks(my_data, n):    
    for i in range(0, len(my_data), n):
        yield my_data[i:i+n]
        
   
def calc_checksum(data):
    g_poly = 0x04C11DB7 # defined on web fro CRC32
    result=""
    crc = binascii.crc32(data)&0xFFFFFFFF
    for i in range(8):
        b = (crc >> (8*i)) & 0xFF
        print("b is ", b)
        result += ('%02X\n' % b)
    return result
    
#------End Of Funstions Used------# 
#SourceAddress = hexlify(getaddrinfo(clientSocket))
DestinationAddress = 0x2EE0
flag = 0x7E
Header = flag
Trailer = ""

file = open("TestData.txt", "rb")                       # Open File For Reading And Writing
data = file.read(3360)
FileRemaining = len(data)                               # Remaining Length Of Text To Be Sent
Sequence = 0
ACK_Sequence = 0
ACK = False

while FileRemaining > 0:   # while there is still data to be TX'd
    for chunk in chunks(data, 8):   #sending only 8 bits at a time
        FileRemaining -= len(chunk)
        #print("Chunk: ", chunk)
        check = calc_checksum(chunk)
        Trailer +=  flag + check
        Header = flag + Sequence + DestinationAddress + SourceAddress 
        print("CheckSum: ", Check)
        packet = chunk + Header + Trailer
        clientSocket.send(packet)
        print("Packet Sent, Waiting on ACK From Server...")
        while ACK == False:
            print "In ACK while loop"
            acknowledgement = clientSocket.recv(8)
            clientSocket.settimeout(10)
            print "ACK", acknowledgement
            if acknowledgement == "true":
                ACK = True
                print("Received ACK frame from server - packet ", Sequence, " sent successfully.")
            elif acknowledgement == "false":
                clientSocket.send(chunk)
                print("Just resent the packet with seq num ", Sequence)
            
        Sequence += 1
        ACK = False
        ACK_Sequence += 1

print("Stopped Generating New Frames - End Of Data File!")
print("Sending Completed")
file.close()
clientSocket.close()
