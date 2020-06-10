#!/usr/bin/python
import socket
import json

DN=1
HOST='localhost'
PORT=12900+DN

# Connect to AVS4000 API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# Create REQ
REQ=["get",["ref","ddc","duc","rxstat","txstat"]];

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list

if RSP[0]==False:
    print("Failed!");
else:
    # The following processes the returned MAP
    rval=RSP[1];                   # Info is a MAP of Group MAPs
    for g in sorted(rval.keys()):  # Each entry in the MAP is a Group Name:MAP pair
        grp=rval[g];               # The Group MAP
        # Each Param in Group MAP is a Param Name:value pair
        for p in sorted(grp.keys()):
            name=g+"."+p;          # Create a grp.param name
            val=grp[p]
            # print grp.param name and value
            print("{:>25s}: {}".format(name,val));
