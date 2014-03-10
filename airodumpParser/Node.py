import urllib2
import urllib
import requests
from datetime import datetime, date, time    

class Node(object):

    def __init__(self, kind="Router", params = list()):

        if not params:
            print "No params"
            self.kind = kind    
            self.BSSID = " "
            self.firstTimeSeen = " "
            self.lastTimeSeen = " "
            self.Channel = " "
            self.Speed = " "
            self.Privacy = " "
            self.Power = ""
            self.ip = " "    
            self.ESSID = " "    
            self.probedESSID = " "  
            self.alive = None
            self.forDB = dict()

        elif kind == "Router":
            # print "Router"
            # params = line.split(",")
            self.kind = "Router"
            self.BSSID = params[0].strip()
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2].strip()
            self.Channel = int(params[3])
            self.Speed = int(params[4])
            self.Privacy = params[5]
            self.Power = int(params[8])
            self.ESSID = params[13]
            self.AP = "None"
            self.probedESSID = " "
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,self.ESSID]
            self.forDB =  dict([ ("kind",self.kind) , ("bssid",self.BSSID) , ("power",self.Power) , ("speed",self.Speed) , ("essid",self.ESSID) ])  
            self.forDB["times"]  = [ self.firstTimeSeen , self.lastTimeSeen ]
            self.alive = True;

        else:
            # print "Client"
            # params = line.split(",")
            self.kind = "Client"
            self.BSSID = params[0].strip()
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2].strip()
            self.Channel =  -1
            self.Speed = -1
            self.Privacy = " "
            self.AP = params[5]
            # print params[8]
            self.Power = int(params[3])
            #TODO: make list of all networks
            self.ESSID = " "
            self.probedESSID = params[6:]            #, ("times",self.lastTimeSeen)       # ("AP", (self.AP,self.lastTimeSeen)) 
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,":".join(self.probedESSID)]
            self.forDB = dict([ ("kind",self.kind) , ("bssid",self.BSSID) ,("power",self.Power), ("essid",self.AP)  , ("probed",self.probedESSID) ])
            self.forDB["times"]  = [ self.firstTimeSeen , self.lastTimeSeen ]
            self.alive = True;

    def printParams(self):
        print self.kind
        print self.BSSID
        print self.firstTimeSeen
        print self.lastTimeSeen
        print self.Channel
        print self.Speed
        print self.Privacy
        print self.Power
        # print self.ip
        print self.ESSID
        print self.probedESSID
        print self.alive

    def trimParams(self):
        self.kind = self.kind.strip()
        self.BSSID = self.BSSID.strip()
        self.firstTimeSeen= self.firstTimeSeen.strip()
        self.lastTimeSeen = self.lastTimeSeen.strip()
        self.Channel
        self.Speed
        self.Privacy = self.Privacy.strip()
        self.Power
            # print self.ip
        self.ESSID = self.ESSID.strip()
        self.probedESSID = self.probedESSID
	
    def updateRouterNode(self, params):
        print "Updating Router : " + self.BSSID 
        # print "Updating Router : " + self.BSSID + " from time : " + self.lastTimeSeen + " to time : "+ params[2]
        # self.kind = "Router"
        # self.BSSID = params[0]
        self.alive = True
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2].strip()
        self.Channel = int(params[3])
        self.Speed = int(params[4])
        self.Privacy = params[5]
        # print params[8]
        self.AP = "None"
        self.Power = -int(params[8])
        self.ESSID = params[13]    
        self.probedESSID = " "  
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,self.ESSID]
        self.forDB["times"].append(self.firstTimeSeen)
        self.forDB["times"].append(self.lastTimeSeen)

    def updateClientNode(self, params):
        print "Updating Client : " + self.BSSID + " from time : " + self.lastTimeSeen + " to time : "+ params[2]
        self.alive = True
        print params[6:]
    	# self.kind = "Client"
        # self.BSSID = params[0]
        # print params[8]
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2]
        self.Channel =  -1
        self.Speed = -1
        self.Privacy = " "
        
        self.Power = -int(params[3])
        self.AP = params[5]
        self.ESSID = " "
        self.probedESSID = params[6:] 
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,":".join(self.probedESSID)]
        self.forDB["times"].append(self.firstTimeSeen)
        self.forDB["times"].append(self.lastTimeSeen)

    def hasTimeChanged(self, newTime): 
        if self.lastTimeSeen.strip() == newTime.strip():
            return False
        else:
            # print "Time changed "+ self.lastTimeSeen + " to " + newTime
            return True

    def wrapForOsc(self):
        return " , ".join(self.forOSC)

    def postToDB(self,url):

        r = requests.get(url+"/write", params=self.forDB)
        try:
            print r.json()

        except ValueError: #bail if there is no argument for 'devicename' submitted
            print "Val error" 
        else:
            print "sent"  



if __name__ == '__main__' :

    url = 'http://localhost:8080'
    routerLine = "1C:AF:F7:D6:0E:0F, 2014-03-02 20:22:49, 2014-03-02 20:25:48,  3,  54, WEP , WEP,   , -34,      143,     1411,   0.  0.  0.  0,  16, Flying Spaghetti,"
    clientLine = "70:DE:E2:8C:47:53, 2014-03-02 20:23:29, 2014-03-02 20:23:29, -44,        6, 1C:AF:F7:D6:0E:0F,"
    clientLine2 = "00:24:2B:05:D1:A8, 2014-02-27 13:49:05, 2014-02-27 14:03:55, -95,      159, (not associated) , Carolyn Protass's Network,Melissa Protass's Network,DanaWireless,orchardhousecafe"

    clientLine2.strip()
    clientLine2 = clientLine2.replace("\r\n"," ")
    params = clientLine2.split(',')
    node = Node("Client", params)
    # try:
    print node.postToDB(url)

    # except ValueError: #bail if there is no argument for 'devicename' submitted
    #     print "THERE WAS AN ERROR" 
    # else:
    #     print sent  

    # routerLine.strip()
    # routerLine = routerLine.replace("\r\n"," ")
    # params = routerLine.split(',')
    # node = Node("Router",params)
    # try:
    #     print node.postToDB(url)

    # except ValueError: #bail if there is no argument for 'devicename' submitted
    #     print "THERE WAS AN ERROR" 
    # else:
    #     print sent
    



