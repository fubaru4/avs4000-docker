#!/usr/bin/python
import socket
import json
import os

DN=1
HOST='localhost'
PORT=12900+DN
TX_PORT=12800+DN

# Connect to AVS4000 API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
P={};                    # Set REQ Map
TX={};                   # TX Group Map
TXD={};                  # TXDATA Group Map
TX["sampleRate"]=15e6    # TX Sample Rate
TXD["conEnable"]=True;   # enable RX Data Connection
TXD["conType"]="tcp";    # Specify to use TCP
TXD["conPort"]=TX_PORT;  # Specify TCP Port to listen on
TXD["useV49"]=False;     # Receive Raw IQ Data
TXD["run"]=True;         # Start the stream
P["tx"]=TX;              # Add TX Group Map to REQ
P["txdata"]=TXD;         # Add TXDATA Group Map to REQ

REQ=['set',P];           # Create REQ for SET Command

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

# Use SOCAT utitiltiy to connect to TCP TX Data Socket
# read data from file '/dev/zero'.
os.system("socat -u FILE:/dev/zero TCP:localhost:%d &"%(TX_PORT))

