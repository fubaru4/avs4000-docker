#!/usr/bin/python
import sys
import socket
import json
import os
import time

def Success(RSP):
    if type(RSP) is list:
        if len(RSP)>0:
            return RSP[0];
    return False;

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

def SendREQ(REQ):
    sock.send(json.dumps(REQ));
    str=sock.recv(16*1024);
    if str[-1]!='\n':
        # don't have a LF?  then read more data
        buf=sock.recv(16*1024);
        str=str+buf;
    return json.loads(str);

def Get(grp,param):
    RSP=SendREQ(["get",grp]);
    if Success(RSP):
        return Fetch(RSP[1],grp,param);
    return None;

def GetParamDirect(grp,param):
    grpDotParam = grp + "." + param;
    RSP = SendREQ(["get",grpDotParam]);
    if Success(RSP):
        #Assuming in this mode, List of Len() = 2
        return RSP[1];
    return None;

# GetP(g,p) will return a pending value of a grp.param
def GetP(grp,param):
    RSP=SendREQ(["getp",grp]);
    if Success(RSP):
        return Fetch(RSP[1],grp,param);
    return None;

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

def SetRefMode(modeStr):
    if (Set('ref','mode',modeStr) != True):
        sys.exit('Setting Reference Mode Failed!');
    else:
        print('Reference Mode set to ' + REF_MODE + '.');
        return True;

def CheckRefLock():
    if (GetParamDirect('ref','lock') != True):
        sys.exit('Reference is not locked! Check refernece input!');
    else:
        print('Reference is Locked.');
        return True;


def SetPPSSel(ppsSelStr):
    if (Set('ref','PPSSel',ppsSelStr) != True):
        sys.exit('Setting PPSSel Failed!');
    else:
        print('PPSSel Set to ' + PPS_SEL + '.');

def SetMstrSampMode(modeStr):
    if (Set('master','SampleRateMode',modeStr) != True):
        sys.exit('Setting Master Sample Rate Mode Failed!');
    else:
        print('Master Sample Rate Mode set to ' + MSTR_SAMP_MODE + '.');

def SetMstrSampRate(MSr):
    if (Set('master','SampleRate',MSr) != True):
        sys.exit('Setting Master Sample Rate Failed!');
    else:
        print('Master Sample Rate set to ' + str(MSr) + '(Hz).');

def SetRxSampRate(RSr):
    if (Set('rx','SampleRate',RSr) != True):
        sys.exit('Setting RX Sample Rate Failed!');
    else:
        print('RX Sample Rate set to ' + str(RSr) + '(Hz).');

def SysSync():
    if (Set('ref','sysSync',True) != True):
        sys.exit('sysSync() Failed!');
    else:
        print('sysSync() Successful');

def SetTimebase():
    if (Set('ref','TimeBase','Host') != True):
        sys.exit('SetTimebase() Failed!');
    else:
        print('SetTimebase() Successful');


def SetRxUserDelay(dly):
    if (Set('rx','UserDelay',dly) != True):
        sys.exit('Setting RX User Delay Failed!');
    else:
        print('RX User Delay set to ' + str(dly) + '.');

def SetRxStartMode(smode):
    if (Set('rx','StartMode',smode) != True):
        sys.exit('Setting RX Start Mode Failed!');
    else:
        print('RX Start Mode set to ' + smode + '.');

def SetRxFreq(rxFreq):
    if (Set('rx','Freq',rxFreq) != True):
        sys.exit('Setting RX Frequency Failed!');
    else:
        print('RX Frequency set to ' + str(rxFreq) + '(Hz).');

def SetDdcFreq(ddcFreq):
    if (Set('ddc','Freq',ddcFreq) != True):
        sys.exit('Setting DDC Frequency Failed!');
    else:
        print('DDC Frequency set to ' + str(ddcFreq) + '(Hz).');

        

def startV49Rx(tcp_rx_port):
    # Create REQ
    P={};                    # Set REQ Map
    RX={};                   # RX Group Map
    RXD={};                  # RXDATA Group Map
    RXD["conEnable"]=True;   # enable RX Data Connection
    RXD["conType"]="tcp";    # Specify to use TCP
    RXD["conPort"]=tcp_rx_port;  # Specify TCP Port to listen on
    RXD["useV49"]=True;     # Receive Raw IQ Data
    RXD["run"]=True;         # Start the stream
    P["rxdata"]=RXD;         # Add RXDATA Group Map to REQ

    REQ=['set',P];           # Create REQ for SET Command

    sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
    str=sock.recv(8192);        # Receive the RSP
    RSP=json.loads(str);        # Parse JSON to Python list
    return RSP;

def stopRx():
        # Create REQ
        P={};                 # Set REQ Map
        G={};                 # RXDATA Group Map
        G["conEnable"]=False; # Disable RX Data Connection
        G["run"]=False;       # Stop the RX Data stream
        P["rxdata"]=G;        # Add RXDATA Group Map to REQ
        #print(P);
        REQ=['set',P];        # Create REQ for SET Command

        sock.send(json.dumps(REQ)); # Convert REQ to JSON and send on socket
        str=sock.recv(8192);        # Receive the RSP
        RSP=json.loads(str);        # Parse JSON to Python list
        return RSP;


DN=1
HOST='localhost'
API_CTRL_PORT=12900+DN
RX_DATA_PORT=12700+DN

CAP_LEN_SEC = 8;
RF_CENTER_FREQ = 2.4E9
FREQ_OFFSET = 0;
RX_FREQ = RF_CENTER_FREQ + FREQ_OFFSET;
DDC_FREQ = FREQ_OFFSET;
REF_MODE = 'External';
PPS_SEL = 'External';
MSTR_SAMP_MODE = 'Manual';
MSTR_SAMP_RATE = 40e6;
RX_SAMP_RATE = 1e6;
USER_DELAY = 0;
RX_START_MODE = 'OnPPS';

# Connect to AVS4000 API socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((HOST,API_CTRL_PORT));

# Set the Reference to External
SetRefMode(REF_MODE);

# Check the state of the reference lock parameter
CheckRefLock();

# Set the PPS Selection
SetPPSSel(PPS_SEL)

# Set the Master Sample Rate mode
SetMstrSampMode(MSTR_SAMP_MODE)

# If in Manual Mode, set the Mastere.SampleRate
if (MSTR_SAMP_MODE == 'Manual'):
    SetMstrSampRate(MSTR_SAMP_RATE);

# Sleep (Just in Case)
#time.sleep(1);

# Perform sysSync of AVS-AVS4000
SysSync();

# Set the RX Sample rate
SetRxSampRate(RX_SAMP_RATE);

# Set the SetTimebase
SetTimebase();

# Set RX User Delay
SetRxUserDelay(USER_DELAY);

# Set RX Start mode
SetRxStartMode(RX_START_MODE);

# Set RX Frequency
SetRxFreq(RX_FREQ);

#SetDdcFreq(DDC_FREQ);
SetDdcFreq(DDC_FREQ);

startV49Rx(RX_DATA_PORT);


# Use SOCAT utitiltiy to connect to TCP RX Data Socket
# save data to a new file 'rx.out'.
os.system("socat -u TCP:localhost:%d CREATE:rxTsCap.v49 &"%(RX_DATA_PORT));

# Use SOCAT utitiltiy to connect to TCP TX Data Socket
# read data from file '/dev/zero'.
#os.system("socat -u TCP:localhost:12914 FILE:/dev/null &")


time.sleep(CAP_LEN_SEC);

stopRx();
