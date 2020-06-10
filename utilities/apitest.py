#!/usr/bin/python
import socket
import json

# This script performs a very basic API Test
# It tests all of the core API commands
# it does assume an AVS4000 since it references AVS4000 specific parameters
# A more comprehensive test script should probably be written
# that tests individual API parameters for the AVS4000
DN=1
HOST="localhost"
PORT=12900+DN

# Connect to JSON API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,PORT));

# API Test

# SendREQ sends a REQ and returns the RSP
def SendREQ(REQ):
    sock.send(json.dumps(REQ));
    str=sock.recv(16*1024);
    if str[-1]!='\n':
        # don't have a LF?  then read more data
        buf=sock.recv(16*1024);
        str=str+buf;
    return json.loads(str);

def Success(RSP):
    if type(RSP) is list:
        if len(RSP)>0:
            return RSP[0];
    return False;

def ExpectError(RSP,ERR):
    if type(RSP) is list:
        if len(RSP)>1 and RSP[0]==False and RSP[1]==ERR:
            return True;
    return False;

def TestParse():
    if ExpectError(SendREQ(0),1) and \
       ExpectError(SendREQ("abc"),1) and \
       ExpectError(SendREQ([]),3) and \
       ExpectError(SendREQ([0]),1) and \
       ExpectError(SendREQ(["abc"]),2) and \
       ExpectError(SendREQ(True),1)and \
       ExpectError(SendREQ(False),1)and \
       ExpectError(SendREQ({}),1):
           return True;
    return False;

def TestGetError():
    RSP=SendREQ(["geterr"]);
    if Success(RSP):
        E=RSP[1];
        if len(E)>=15 and len(E[0])==2 and E[14][0]==14:
            return True;
    return False;

def Match(cmd,list):
    for c in list:
        if c[0]==cmd:
            return True;
    return False;

def TestGetCmd():
    RSP=SendREQ(["getcmd"]);
    if Success(RSP):
        C=RSP[1];
        if len(C)>=8 and \
            Match("GET",C) and Match("GETP",C) and \
            Match("SET",C) and Match("SETN",C) and \
            Match("COMMIT",C) and Match("DISCARD",C) and \
            Match("GETERR",C) and Match("GETCMD",C) and \
            Match("INFO",C):
            return True;
    return False;

# GetAll() returns a dictionary of all API parameter values
def GetAll():
    RSP=SendREQ(["get"]);
    if Success(RSP):
        return RSP[1];
    return None;

# InfoAll() returns a dictionary of INFO for all API parameters
def InfoAll():
    RSP=SendREQ(["info"]);
    if Success(RSP):
        return RSP[1];
    return None;

# Set(g,p,v) will set the value of a single grp.param
def Set(grp,param,val):
    return Success(SendREQ(["set",{grp:{param:val}}]));

# SetN(g,p,v) will set the value of a single grp.param without commit
def SetN(grp,param,val):
    return Success(SendREQ(["setn",{grp:{param:val}}]));

# Commit pending changes
def Commit():
    return Success(SendREQ(["commit"]));

# Discard pending changes
def Discard():
    return Success(SendREQ(["discard"]));

# Fetch will retrieve the value of a grp.param from a dictionary/map
def Fetch(map,grp,param):
    # This function is used to retrieve a grp.param from the map
    # This is done to support case insensitivity
    for g in map.keys():
        if g.lower()==grp.lower():
            for p in map[g].keys():
                if p.lower()==param.lower():
                    return map[g][p];
    return None;

# Get(g,p) will return a value of a grp.param
def Get(grp,param):
    RSP=SendREQ(["get",grp]);
    if Success(RSP):
        return Fetch(RSP[1],grp,param);
    return None;

# GetP(g,p) will return a pending value of a grp.param
def GetP(grp,param):
    RSP=SendREQ(["getp",grp]);
    if Success(RSP):
        return Fetch(RSP[1],grp,param);
    return None;

nGroup=0;
nParam=0;

# Basic Test of GET command
def TestGet():
    G=GetAll(); # Get all groups
    if len(G)>0:
        global nParam,nGroup;
        # for now, just count the groups and the parameters
        nParam=0;
        nGroup=len(G);
        for g in G:
            nParam = nParam + len(g)
#            print("Groups={} Total Params={}".format(nGroup,nParam));
        if nGroup>=10 and nParam>=43:
            return True;
    return False;

# Basic Test of INFO command
def TestInfo():
    G=InfoAll();
    if len(G)>0:
        # count the groups and parameters and compare to the TestGet results
        nInfoParam=0;
        nInfoGroup=len(G);
        for g in G:
            nInfoParam = nInfoParam + len(g)
#        print("GET: Groups={} Total Params={}".format(nGroup,nParam));
#        print("INFO: Groups={} Total Params={}".format(nInfoGroup,nInfoParam));
        if nGroup==nInfoGroup and nParam==nInfoParam:
            return True;
    return False;

# Test SetN and GetP
def TestSetNGetP():
    oldVal=Get("rx","freq");    # fetch old value
    val=oldVal+0.1e9;           # new value is different than old value
    return SetN("rx","freq",val) and GetP("rx","freq")==val and \
           Get("rx","freq")==oldVal;

# Test Discard by using SetN and GetP
def TestDiscard():
    oldVal=Get("rx","freq");
    val=oldVal+0.1e9;
    return SetN("rx","freq",val) and GetP("rx","freq")==val and \
           Discard() and GetP("rx","freq")==None and \
           Get("rx","freq")==oldVal;

# Test Commit, by using SetN, GetP & Get
def TestCommit():
    val=1.3e9;
    return SetN("rx","freq",val) and GetP("rx","freq")==val and \
           Get("rx","freq")!=val and Commit() and Get("rx","freq")==val;

# Test a basic SET
def TestSet():
    oldVal=Get("rx","freq");
    val=2.4e9
    return oldVal!=val and Set("rx","freq",val) and Get("rx","freq")==val;

# Test Master Sample Rate Auto Mode
def TestAutoMode1():
    # Must first set auto mode prior to setting sample rates
    return Set("master","sampleratemode","auto") and \
           SetN("rx","samplerate",18e6) and SetN("tx","samplerate",4.5e6) and \
           Commit() and Get("master","samplerate")==36e6;

# Test Master Sample Rate Auto Mode failure
def TestAutoMode2():
   # This samplerate combination will not be able to find a master sample rate
   # When this happens, the Commit will fail
   return Set("master","sampleratemode","auto") and \
          SetN("rx","samplerate",4.7e6) and SetN("tx","samplerate",1e6) and \
          Commit()==False and Discard();

# Test Master Auto mode using a single SET
def TestAutoMode3():
    # Must first set auto mode prior to setting sample rates
    # Then we use a single SET ecommand to set both RX & TX sample rates
    return Set("master","sampleratemode","auto") and \
           Success(SendREQ(["set",{"rx":{"samplerate":2.1e6}, \
                                   "tx":{"samplerate":1.5e6}}])) and \
           Get("master","samplerate")==42e6;


TESTS=[ ["Test Parse Failures", TestParse], \
        ["Test GETCMD", TestGetCmd], \
        ["Test GETERR", TestGetError], \
        ["Test GET", TestGet], \
        ["Test INFO", TestInfo], \
        ["Test SETN & GETP", TestSetNGetP], \
        ["Test DISCARD", TestDiscard], \
        ["Test COMMIT", TestCommit], \
        ["Test SET", TestSet], \
        ["Test Master Auto Mode #1", TestAutoMode1], \
        ["Test Master Auto Mode #2", TestAutoMode2], \
        ["Test Master Auto Mode #3", TestAutoMode3], \
      ]

for t in TESTS:
    print("{:<30s} {}".format(t[0],"PASS" if t[1]() else "FAIL"));

print("nGroup={} nParam={}".format(nGroup,nParam));
