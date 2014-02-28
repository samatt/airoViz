    

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

        elif kind == "Router":
            # print "Router"
            # params = line.split(",")
            self.kind = "Router"
            self.BSSID = params[0]
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2]
            self.Channel = int(params[3])
            self.Speed = int(params[4])
            self.Privacy = params[5]
            self.Power = -int(params[8])
            self.ESSID = params[13]    
            self.probedESSID = " "
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.ESSID]

        else:
            # print "Client"
            # params = line.split(",")
            self.kind = "Client"
            self.BSSID = params[0]
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2]
            self.Channel =  -1
            self.Speed = -1
            self.Privacy = " "
            # print params[8]
            self.Power = -int(params[3])
            #TODO: make list of all networks
            self.ESSID = " "
            self.probedESSID = params[6:]
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power)," ".join(self.probedESSID)]

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
        print "Updating Router : " + self.BSSID + " from time : " + self.lastTimeSeen + " to time : "+ params[2]
        self.kind = "Router"
        self.BSSID = params[0]
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2]
        self.Channel = int(params[3])
        self.Speed = int(params[4])
        self.Privacy = params[5]
        # print params[8]
        self.Power = -int(params[8])
        self.ESSID = params[13]    
        self.probedESSID = " "  
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.ESSID]

    def updateClientNode(self, params):
        print "Updating Client : " + self.BSSID + " from time : " + self.lastTimeSeen + " to time : "+ params[2] + " networks : " 
        print params[6:]
    	self.kind = "Client"
        self.BSSID = params[0]
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2]
        self.Channel =  -1
        self.Speed = -1
        self.Privacy = " "
        # print params[8]
        self.Power = -int(params[3])
        #TODO: make list of all networks
        self.ESSID = " "
        self.probedESSID = params[6:] 
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power)," ".join(self.probedESSID)]


    def hasTimeChanged(self, newTime): 
        if self.lastTimeSeen == newTime:
            return False
        else:
            return True

    def wrapForOsc(self):
        return " , ".join(self.forOSC)


# TODO: Add params
#     //    string Cipher;
#     //    string Authentication;
#     //    int numBeacons;
#     //    int numIV;
#     //Client only    
# //    Station MAC,
# //   int  numPackets;

if __name__ == '__main__' :

    print 'Im a node'
