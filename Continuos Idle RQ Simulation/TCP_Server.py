#
# Breandan Kerin
# 14310166
# TCP Server
#
from socket import *
import binascii

ACK = "true"
NACK = "false"

#-------- Setting Up Our Sockets --------#
buf = 8
serverPort = 12000
HOST = ''

try:
        serverSocket = socket(AF_INET,SOCK_STREAM)
except socket.error:
        print("Socket Failed To Be Created")
        exit(1)
        
print("Socket Created Successfully")
serverSocket.bind((HOST, serverPort))
serverSocket.listen(1)  #begins to listen and sets the max. accept rate to 1
print ("The Server Is Ready To Receive Your Data")

 
#-------- Below I Will Have to Deal With Data --------#
file = open("TestDataOutput", "wb")   # open the output file and prep. for writing to it
connectionSocket, addr = serverSocket.accept()
print("Connection Was Successful")              #Server Has Connected to Client

while 1:        # loop to infinity
        data = connectionSocket.recv(buf)       
        print("Some Piece Of Data Has Been Recieved")
	capitalizedSentence = data.upper()
	print("recieved from client:", str(data))
        connectionSocket.send(ACK)
        print("Sent ACK frame back to client")	
#	connectionSocket.send(capitalizedSentence)
        file.write(data)
        #data = ""
file.close()
connectionSocket.close()
