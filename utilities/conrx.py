#!/usr/bin/python
import socket
import json
import os

# HOST='192.168.1.5'
DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

P={};
G={};
G["conEnable"]=True;
G["conPort"]=RX_PORT;
G["conType"]="tcp";
G["testPattern"]=True;
G["run"]=False;
P["rxdata"]=G;

REQ=['set',P];

sock.send(json.dumps(REQ));
str=sock.recv(8192);
RSP=json.loads(str);
print (RSP);
