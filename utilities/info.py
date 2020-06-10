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
REQ=['info'];

sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
str=sock.recv(8192);        # Receive the RSP
RSP=json.loads(str);        # Parse JSON to Python list

if RSP[0]==False:
    print("Failed!");
else:
    # The following processes the returned MAP
    info=RSP[1];                   # Info is a MAP of Group MAPs
    for g in sorted(info.keys()):  # Each entry in the MAP is a Group Name:MAP pair
        grp=info[g];               # The Group MAP
        # Each Param in Group MAP is a Param Name:String pair
        for p in sorted(grp.keys()):
            name=g+"."+p;           # Create a grp.param name
            pos=grp[p].find("[");   # Look to se if a range is contained in info
            r="";
            if pos<0:               # No range provided
                desc=grp[p];
            else:
                desc=grp[p][:pos];  # Break out the description portion of info
                r=grp[p][pos:];     # Break out the range portion of the info
            # print grp.param name and description
            print("{:>25s}: {:s}".format(name,desc));
            if len(r)>0:
                # if there is a range, print it on a line by itself
                print("{:>25s}  {:s}".format("",r));
