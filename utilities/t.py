#!/usr/bin/python
import socket
import json
import os
import time

DN=1
HOST='localhost'
PORT=12900+DN
RX_PORT=12700+DN
TX_PORT=12800+DN
RATE=20e6

# Connect to AVS4000 API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
P={};                    # Set REQ Map
RX={};                   # RX Group Map
RXD={};                  # RXDATA Group Map
DDC={};                  # DDC Group Map
DDC["outgain"]=3.1;      # DDC Out Gain
DUC={};                  # DUC Group Map
DUC["outgain"]=3.8;      # DUC Out Gain
RX["sampleRate"]=RATE;   # RX Sample Rate
RXD["conEnable"]=True;   # enable RX Data Connection
RXD["conType"]="tcp";    # Specify to use TCP
RXD["conPort"]=RX_PORT;  # Specify TCP Port to listen on
RXD["useV49"]=True;      # Receive Raw IQ Data
RXD["run"]=True;         # Start the stream
P["rx"]=RX;              # Add RX Group Map to REQ
P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ
TX={};                   # TX Group Map
TXD={};                  # TXDATA Group Map
TX["sampleRate"]=RATE;   # TX Sample Rate
TXD["conEnable"]=True;   # enable RX Data Connection
TXD["conType"]="tcp";    # Specify to use TCP
TXD["conPort"]=TX_PORT;  # Specify TCP Port to listen on
TXD["useV49"]=True;      # Receive Raw IQ Data
TXD["run"]=True;         # Start the stream
P["tx"]=TX;              # Add TX Group Map to REQ
P["txdata"]=TXD;         # Add TXDATA Group Map to REQ
P["ddc"]=DDC;
P["duc"]=DUC;

REQ=['set',P];           # Create REQ for SET Command

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

REQ=['get','ddc']
sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

REQ=['get','duc']
sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP

# Use SOCAT utitiltiy to connect to TCP RX Data Socket
# save data to a new file 'rx.out'.
os.system("socat -u FILE:/dev/zero TCP:localhost:%d &"%(TX_PORT))
os.system("socat -u TCP:localhost:%d FILE:/dev/null &"%(RX_PORT))

time.sleep(10)

# Create REQ
P={};                    # Set REQ Map
RXD={};                  # RXDATA Group Map
RXD["conEnable"]=False;  # disable RX Data Connection
RXD["run"]=False;        # Stop the stream
P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ
TXD={};                  # TXDATA Group Map
TXD["conEnable"]=False;  # disable TX Data Connection
TXD["run"]=False;        # Stop the stream
P["txdata"]=TXD;         # Add TXDATA Group Map to REQ

REQ=['set',P];           # Create REQ for SET Command

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list
print (RSP);                # Print the RSP


