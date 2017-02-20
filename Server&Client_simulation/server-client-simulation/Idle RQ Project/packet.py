#
# General functions for manipulation the data fields
#

import CRC
import random
from binascii import hexlify

# -------Functions used--------
def chunks(my_data, n):                               # breaks all the data into chunks of size n
    for i in range(0, len(my_data), n): # for a chunk in data of length n
        yield my_data[i:i+n]

def packet(data, seq, ack_field):        ## chunk, seq, '00'
    flag = "7E"
    seq_string=str(seq)
    print("Frame num: ", seq_string)
    print("Data: ", data)
    crc = CRC.calc_checksum(data)
    print("Checksum (frame) ", seq_string, ": ", crc)        # when the server does a checksum on this chunk, should yield same result - send ack
    data = str(data)

    header = flag + "-" + seq_string + "-" + ack_field
    trailer = crc + "-" + flag
    packet = header + "-" + data + "-" + trailer
    return str(packet)


