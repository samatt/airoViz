import urllib2
import urllib
import requests
import logging
from datetime import datetime, date, time, timedelta

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
            self.kind = "Router"
            self.BSSID = params[0].strip()
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2].strip()
            self.Channel = int(params[3])
            self.Speed = int(params[4])
            self.Privacy = params[5]
            self.Power = self.updatePower(params[8])
            self.ESSID = params[13]
            self.AP = "None"
            self.probedESSID = " "
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,self.ESSID]
            self.forDB =  dict([ ("kind",self.kind) , ("bssid",self.BSSID) , ("power",self.Power) , ("speed",self.Speed) , ("essid",self.ESSID) ])
            self.forDB["times"]  = [ self.firstTimeSeen , self.lastTimeSeen ]
            self.alive = True;

        else:
            self.kind = "Client"
            self.BSSID = params[0].strip()
            self.firstTimeSeen = params[1]
            self.lastTimeSeen = params[2].strip()
            self.Channel =  -1
            self.Speed = -1
            self.Privacy = " "
            self.AP = params[5]
            self.Power = self.updatePower(params[3])

            #TODO: make list of all networks
            self.ESSID = " "
            self.probedESSID = params[6:]
            self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,":".join(self.probedESSID)]
            self.forDB = dict([ ("kind",self.kind) , ("bssid",self.BSSID) ,("power",self.Power) , ("probed",self.probedESSID) ])
            self.forDB["times"]  = [ self.firstTimeSeen , self.lastTimeSeen ]

            #using the pipe to be keep track of when
            #the client was associated to a router and update if it changes
            newAP = [self.AP + "|" + self.lastTimeSeen]
            self.forDB["essid"]= newAP

            self.alive = True;

    def updatePower(self, newValue):
        newValue = int(newValue)
        if newValue >= -1 and newValue <=    0:
            return -128
        else:
            return newValue

    def printParams(self):
        print self.kind
        print self.BSSID
        print self.firstTimeSeen
        print self.lastTimeSeen
        print self.Channel
        print self.Speed
        print self.Privacy
        print self.Power
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
        self.ESSID = self.ESSID.strip()
        self.probedESSID = self.probedESSID
        trimProbe = []
        for probe in self.probedESSID:
            probe = probe.strip()
            trimProbe.append(probe)

        self.probedESSID = trimProbe

    def updateRouterNode(self, params):

        self.alive = True
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2].strip()
        self.Channel = int(params[3])
        self.Speed = int(params[4])
        self.Privacy = params[5]
        self.AP = "None"
        self.Power = self.updatePower(params[8])
        self.ESSID = params[13]
        self.probedESSID = " "

        #Updates for DB
        self.forDB["power"] = self.Power

        #Removing these because they seem redundent for the real time app.
        # self.forDB["times"].append(self.firstTimeSeen)
        # self.forDB["times"].append(self.lastTimeSeen)
        self.forDB["times"] =self.lastTimeSeen

        #Updates for OSC
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,self.ESSID]

    def updateClientNode(self, params):

        self.alive = True
        self.firstTimeSeen = params[1]
        self.lastTimeSeen = params[2]
        self.Channel =  -1
        self.Speed = -1
        self.Privacy = " "
        self.Power = self.updatePower(params[3])
        self.ESSID = " "
        self.probedESSID.append( params[6:])
        if self.AP == params[5]:
            pass
        else:
            logging.debug("AP updated from : " +  self.AP + " to "+params[5] +"|"+self.lastTimeSeen)
            self.AP = params[5]
            #using the pipe to be keep track of when the client was associated to a router and update if it changes
            newAP = self.AP + "|" + self.lastTimeSeen
            self.forDB["essid"].append(newAP)

        newProbe = []
        for probe in self.probedESSID:
            if probe == " ":
                pass
            elif probe in self.probedESSID:
                pass
            else:
                probe = probe.strip()
                newProbe.append(probe)

        self.probedESSID = newProbe
        #Updates for DB
        self.forDB["power"] = self.Power
        # self.forDB["times"].append(self.firstTimeSeen)
        # self.forDB["times"].append(self.lastTimeSeen)
        self.forDB["times"] = self.lastTimeSeen

        # Updates for OSC
        self.forOSC = [self.kind, self.BSSID,self.firstTimeSeen,self.lastTimeSeen, str(self.Channel),str(self.Speed),self.Privacy,str(self.Power),self.AP,":".join(self.probedESSID)]

        if len(newProbe) > 0:
            logging.debug("Updating probes for Client : " + self.BSSID)
            self.forDB["probed"].append(newProbe)

    def hasTimeChanged(self, newTime):

        try:
          lastTimeSeen = datetime.strptime(self.lastTimeSeen.strip(), "%Y-%m-%d %H:%M:%S")
          curTime = datetime.strptime(newTime.strip(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
          logging.error("invalid time: " +newTime);

        else:

          if (curTime - lastTimeSeen) > timedelta(seconds = 1):
              logging.debug("Time since previous ping for "+self.BSSID +" with "+ self.AP +" : ")
              logging.debug(curTime - lastTimeSeen)
              return True
          else:
              return False

    def wrapForOsc(self):
        return " , ".join(self.forOSC)

    def postToDB(self,url = 'http://localhost:8080'):


        try:
          r = requests.get(url+"/write", params=self.forDB)
        except requests.exceptions.RequestException as e:    # This is the correct syntax
            logging.error("Not Connected")


    def updateDB(self, url = "http://localhost:8080"):


        try:
            r = requests.get(url+"/update", params=self.forDB)
            logging.debug("Updating : "+ self.BSSID)
        except requests.exceptions.RequestException as e:    # This is the correct syntax
            logging.error("Not Connected")



def parseLine(line):
  line.strip()
  line = line.replace("\r\n"," ")
  params = line.split(',')
  node = Node("Client", params)
  print node.printParams()

if __name__ == '__main__' :

    url = 'http://localhost:8080'
    routerLine = "1C:AF:F7:D6:0E:0F, 2014-03-02 20:22:49, 2014-03-02 20:25:48,  3,  54, WEP , WEP,   , -34,      143,     1411,   0.  0.  0.  0,  16, Flying Spaghetti,"
    clientLine = "70:DE:E2:8C:47:53, 2014-03-02 20:23:29, 2014-03-02 20:23:29, -44,        6, 1C:AF:F7:D6:0E:0F,"
    clientLine2 = "00:24:2B:05:D1:A8, 2014-02-27 13:49:05, 2014-02-27 14:03:55, -95,      159, (not associated) , Carolyn Protass's Network,Melissa Protass's Network,DanaWireless,orchardhousecafe"
    clientLine3 = "00:24:2B:05:D1:A8, 2014-02-27 13:49:05, 2014-02-27 14:03:55, -95,      159, (not associated) ,PACE-OPEN,TheatreRow,attwifi,Belkin.4554,Nittany 05,NWS Special Events,Guest,Delacorte,PACE-WIRELESS,LaMaMaBox"

    lines = []
    lines.append(routerLine)
    lines.append(clientLine)
    lines.append(clientLine2)
    lines.append(clientLine3)

    for line in lines:
      parseLine(line)
    # clientLine2.strip()
    # clientLine2 = clientLine2.replace("\r\n"," ")
    # params = clientLine2.split(',')
    # node = Node("Client", params)
    # print node.printParams()
    #
    # routerLine.strip()
    # routerLine = routerLine.replace("\r\n"," ")
    # params = routerLine.split(',')
    # node = Node("Router",params)
    # print node.printParams()
