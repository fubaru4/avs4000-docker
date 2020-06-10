#!/usr/bin/python

# This script demonstrates how to use the AVS4000DM API to list
# all available AVS4000 devices connected to the system.

import socket
import json
import os
import time
import sys

HOST='localhost'

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,12900));
sock.send(json.dumps(["get"]));
str=sock.recv(16*1024);
RSP=json.loads(str);
#print(RSP);
map=RSP[1];
for dn in map['dm']['DNs']:
    d=map["DN%d"%(dn)];
    state="READY" if d['ready'] else "NOT READY";
    print("DN=%d: %s [%s]   %s"%(dn,d['model'],d['sn'],state));
