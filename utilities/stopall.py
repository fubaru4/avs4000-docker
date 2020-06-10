#!/usr/bin/python
import socket
import json
import os
import time

HOST='localhost'
RATE=2e6
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
    dev=Connect(dn);
    Stop(dev);

