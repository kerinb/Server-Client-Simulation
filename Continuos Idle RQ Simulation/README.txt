The aim of this exercise is to simulate a Datalink protocol across an unreliable network link. This program will take a text file containing at least 1024 alphanumeric characters. These programs will use an IPC mechanism (Internet Sockets). 

There are two files in this exercise, they are:
1. A transmitter (Client) that will read the data from a text file, create data-link frames with Headers ( composed of the frame sequence nu,ber, payload length etc) and a trailer (ACK, NACK, checksum) Each fram will contain 8 bytes of input data.A checksum will be calculated using the CRC-16 algorithm which will be stored in the trailer. Once the above is implemented, a gremlin function will be implemented to purposely curropt some of the data transmitted, which leads on to needing to implement continuous-RQ (Selective Repeat) being used. 
2. A reciever (host) that checks the sequence number, checksum and properly handled errors. It will also return an ACK or NACK (when necessary) and will then write the data into an output file.

This program is written in Python 2.7
# My project's README
