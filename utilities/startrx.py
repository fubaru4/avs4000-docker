#!/usr/bin/python
import socket
import json
import os

DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN

# Connect to AVS4000 API socket
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
RXD["useV49"]=False;     # Receive Raw IQ Data
RXD["run"]=True;         # Start the stream
P["rx"]=RX;              # Add RX Group Map to REQ
P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ

REQ=['set',P];           # Create REQ for SET Command

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

# Use SOCAT utitiltiy to connect to TCP RX Data Socket
# save data to a new file 'rx.out'.
os.system("socat -u TCP:localhost:%d CREATE:rx.out &"%(RX_PORT))

