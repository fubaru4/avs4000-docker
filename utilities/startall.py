#!/usr/bin/python
import socket
import json
import os
import time
import sys

HOST='localhost'
RATE=10e6

if len(sys.argv)>1:
    RATE=float(sys.argv[1]);

print("RATE=%6.1f"%(RATE));
devs=[]

def Success(RSP):
    if type(RSP) is list:
        if len(RSP)>0:
            return RSP[0];
    return false;

def GetDNs():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    sock.connect((HOST,12900));
    sock.send(json.dumps(["get"]));
    str=sock.recv(16*1024);
    RSP=json.loads(str);
    print(RSP);
    map=RSP[1];
    return map['dm']['DNs']

# SendREQ sends a REQ and returns the RSP
def SendREQ(dev,REQ):
    sock=dev['sock'];
    sock.send(json.dumps(REQ));
    str=sock.recv(16*1024);
    if str[-1]!='\n':
        # don't have a LF?  then read more data
        buf=sock.recv(16*1024);
        str=str+buf;
    return json.loads(str);

def Connect(DN):
    dev={};
    dev['port']=12900+DN
    # Connect to AVS4000 API socket
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    sock.connect((HOST,dev['port']));
    dev['sock']=sock;
    dev['rxport']=12700+DN
    dev['txport']=12800+DN
    return dev;

def StartLoopback(DN):
    dev=Connect(DN);
    devs.append(dev);
    # Create REQ
    P={};                    # Set REQ Map
    RX={};                   # RX Group Map
    RXD={};                  # RXDATA Group Map
    RX["sampleRate"]=RATE;   # RX Sample Rate
    RXD["conEnable"]=True;   # enable RX Data Connection
    RXD["conType"]="tcp";    # Specify to use TCP
    RXD["conPort"]=dev['rxport'];  # Specify TCP Port to listen on
#    RXD["useV49"]=True;      # Receive Raw IQ Data
    RXD["useV49"]=False;     # Receive Raw IQ Data
    RXD["run"]=True;         # Start the stream
    P["rx"]=RX;              # Add RX Group Map to REQ
    P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ
    TX={};                   # TX Group Map
    TXD={};                  # TXDATA Group Map
    TX["sampleRate"]=RATE;   # TX Sample Rate
    TXD["conEnable"]=True;   # enable RX Data Connection
    TXD["conType"]="tcp";    # Specify to use TCP
    TXD["conPort"]=dev['txport'];  # Specify TCP Port to listen on
#    TXD["useV49"]=True;      # Receive Raw IQ Data
    TXD["useV49"]=False;     # Receive Raw IQ Data
    TXD["run"]=True;         # Start the stream
    P["tx"]=TX;              # Add TX Group Map to REQ
    P["txdata"]=TXD;         # Add TXDATA Group Map to REQ

    REQ=['set',P];           # Create REQ for SET Command
    RSP=SendREQ(dev,REQ);
    print(RSP);
#    if Success(SendREQ(dev,REQ)):
    print('start socat...');
    # Use SOCAT utitiltiy to connect to TCP RX Data Socket
    # save data to a new file 'rx.out'.
    os.system("socat -u FILE:/dev/zero TCP:localhost:%d &"%(dev['txport']))
    os.system("socat -u TCP:localhost:%d FILE:/dev/null &"%(dev['rxport']))

def Stop(dev):
    # Create REQ
    P={};                    # Set REQ Map
    RXD={};                  # RXDATA Group Map
    RXD["conEnable"]=False;  # disable RX Data Connection
    RXD["run"]=False;        # Stop the stream
    P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ
    TXD={};                  # TXDATA Group Map
    TXD["conEnable"]=False;  # disable RX Data Connection
    TXD["run"]=False;        # Stop the stream
    P["txdata"]=TXD;         # Add TXDATA Group Map to REQ

    REQ=['set',P];           # Create REQ for SET Command
    RSP=SendREQ(dev,REQ);
    return Success(SendREQ(dev,REQ));

dnList=GetDNs();
print(dnList);
for dn in dnList:
    StartLoopback(dn);

