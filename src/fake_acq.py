#!/usr/bin/python3

import random
import time
"""
Fake data acquisition. 
Returns a timestamp followed by 512 uint16 values
Uses tabs as separator.

In an optimized version, writing bytes directly to 
stdout would reduce the data size to an int64 (timestamp)
followed by 512 uint16 (2 bytes each), therefore ~ 1 kByte per line.
"""

if __name__ == "__main__":
    N =  512 # Sensor number
    max_val = 2**16 - 1
    freq = 500. # Hz
    while 1:
        print("{}\t".format(int(time.time())), end="")
        for _ in range(N):
            print("{}\t".format(random.randint(0, max_val)), end=""),
        time.sleep(1/freq)
        print()
