#
# Gremlin function
#

import random
import packet


def gremlin(packet, corruptProb, lossProb):
    r = random.random()

    problem = "00"  # not corrupted or dropped
    if r <= (lossProb):
        problem = "01"  # packet was dropped
    elif r <= (corruptProb):
        problem = "10"  # packet was corrupted
    return problem

def corrupt_packet(pkt, seq):
    pkt = constr_packet(bytes("10101010", "UTF-8"), seq, "00") # only the data field needs to be corrupted
    return pkt
