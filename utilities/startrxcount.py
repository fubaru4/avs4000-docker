#!/usr/bin/python
import socket
import json
import os

DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
P={};                    # Set REQ Map
RX={};                   # RX Group Map
RXD={};                  # RXDATA Group Map
RX["sampleRate"]=20e6    # RX Sample Rate
RXD["conEnable"]=True;   # enable RX Data Connection
RXD["conType"]="tcp";    # Specify to use TCP
RXD["conPort"]=RX_PORT;  # Specify TCP Port to listen on
RXD["testPattern"]=True; # Use RX Test Count
RXD["useV49"]=False;     # Receive Raw IQ Data
RXD["run"]=True;         # Start the stream
P["rx"]=RX;              # Add RX Group Map to REQ
P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ

REQ=['set',P];

sock.send(json.dumps(REQ));
str=sock.recv(8192);
RSP=json.loads(str);
print (RSP);
os.system("socat -u TCP:localhost:%d CREATE:rx.out &"%(RX_PORT))
