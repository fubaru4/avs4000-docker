#!/usr/bin/python
import socket
import json
import os

DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN
TX_PORT=12800+DN
RATE=44e6

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
P={};                    # Set REQ Map
RX={};                   # RX Group Map
RXD={};                  # RXDATA Group Map
RX["sampleRate"]=RATE;   # RX Sample Rate
RXD["conEnable"]=True;   # enable RX Data Connection
RXD["conType"]="tcp";    # Specify to use TCP
RXD["conPort"]=RX_PORT;  # Specify TCP Port to listen on
RXD["testPattern"]=False;# Use Real Data
RXD["useV49"]=False;     # Receive Raw IQ Data
RXD["run"]=True;         # Start the stream
P["rx"]=RX;              # Add rX Group Map to REQ
P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ
TX={};                   # TX Group Map
TXD={};                  # TXDATA Group Map
TX["sampleRate"]=RATE;   # TX Sample Rate
TXD["conEnable"]=True;   # enable TX Data Connection
TXD["conType"]="tcp";    # Specify to use TCP
TXD["conPort"]=TX_PORT;  # Specify TCP Port to listen on
TXD["useV49"]=False;     # Receive Raw IQ Data
TXD["run"]=True;         # Start the stream
P["tx"]=TX;              # Add TX Group Map to REQ
P["txdata"]=TXD;         # Add TXDATA Group Map to REQ

REQ=['set',P];

sock.send(json.dumps(REQ));
str=sock.recv(8192);
RSP=json.loads(str);
print (RSP);
os.system("socat -u FILE:/dev/zero TCP:localhost:%d &"%(TX_PORT))
os.system("socat -u TCP:localhost:%d FILE:/dev/null &"%(RX_PORT))

