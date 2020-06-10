#!/usr/bin/python
import socket
import json

DN=1
HOST='localhost'
PORT=12900+DN

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

REQ=['get',''];

sock.send(json.dumps(REQ));
str=sock.recv(8192);
RSP=json.loads(str);
print (RSP[1]);
