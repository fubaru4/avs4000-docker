#!/usr/bin/python
import socket
import json
import os

DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN
TX_PORT=12800+DN

# Connect to AVS4000 API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
P={};                 # Set REQ Map
G={};                 # TXDATA Group Map
G["conEnable"]=False; # Disable TX Data Connection
G["run"]=False;       # Stop the TX Data stream
P["txdata"]=G;        # Add TXDATA Group Map to REQ

REQ=['set',P];        # Create REQ for SET Command

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

