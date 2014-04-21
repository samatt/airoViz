from Node import Node
import sys
import time, threading
import urllib2
import urllib
import requests
from datetime import datetime, date, time
import time
import os
import pickle
import logging

routers = dict()
clients = dict()
routerIdleCount = dict()
clientIdleCount = dict()


def parseLine(params,isRouter):

    if isRouter:
      node = Node("Router",params)
      node.trimParams()
      return node

    elif not isRouter:
      node = Node("Client",params)
      node.trimParams()
      return node


def updateIdleCount(kind,ID):
  if kind == "Router":

    if ID in routerIdleCount:

      routerIdleCount[ID] += 1
      # print "Idle count for  Router" + ID + " : "+ str(routerIdleCount[ID])

    else:
      print 'wtf?'
  else:

    if ID in clientIdleCount:

      clientIdleCount[ID] += 1
      # print "Idle count for  Client" + ID + " : "+ str(clientIdleCount[ID])

    else:
      print 'wtf?'

def addNewNode(kind,ID, params):
  if kind == "Router":
    # print "add routers"
    n =  parseLine(params,True)
    routers[n.BSSID] = n
    routerIdleCount[ID] = 1
    # sender.newNode(n.wrapForOsc(),n.BSSID,"Router")

  else:

    # print "add clients"
    n =  parseLine(params,False)
    clients[n.BSSID] = n
    clientIdleCount[ID] = 1
    # sender.newNode(n.wrapForOsc(),n.BSSID,"Client")

def readFile(fileName):
  isRouter = None
  for line in fileName:

    line.strip()
    line = line.replace("\r\n"," ")
    params = line.split(',')
    # print params
    if len(params) <6 :
      continue

    ID = params[0].strip()
    lastTime = params[2].strip()

    if ID == "BSSID":

      isRouter = True
      continue

    if ID == "Station MAC":

      isRouter = False
      continue

    if isRouter:
      if ID in routers:
        routers[ID].updateRouterNode(params)
      else:
        addNewNode("Router",ID, params)

    else:
      if ID in clients:
        clients[ID].updateClientNode(params)
      else:
        addNewNode("Client",ID,params)


def pickleData():
  # for k,v in clients.iteritems():
    print " No of routers added : "+ str(len(routers))
    print " No of clients added : "  + str(len(clients))
    # print " No of routers total  : "	+ str(len(routers))
    # print " No of clients total  : "	+ str(len(clients))
    print "Pickling files"
    pickle.dump(routers, open( "pickled/routers.p", "wb" ) )
    pickle.dump(clients, open( "pickled/client.p", "wb" ) )
    


def loadPickledData( folder):
  print "loading pickled data"

  routers = pickle.load( open( folder+"/routers.p", "r" ) )
  clients = pickle.load( open( folder+"/client.p", "r" ) )
  print " No of routers : "+ str(len(routers))
  print " No of clients : "  + str(len(clients))
  # return { "routers": routers,"clients":clients}
  return routers,clients

def loadData(rootdir):

  for subdir, dirs, files in os.walk(rootdir):
    size = len(routers)
    sizeC = len(clients)
    for file in files:

      # print subdir+'/'+file
      if ".kismet.csv" not in file and "kismet.netxml" not in file and ".cap" not in file and ".csv" in file:
        csv = open(subdir+"/"+file, 'r')
        print "Reading File :" + file

        readFile(csv)
        csv.close()
        print
      else:
        print "Ignoring file : "+file

def postToDB(url,data):
  i =0
  print type(data[0])
  for k,v in data[0].iteritems():
    print "Im here"
    # data[0][k].postToDB(url)
    # print "Router :" + str(i) + " of "+ str(len(data[0]))
    i+=1

  i =0
  for k,v in data[1].iteritems():
    data[1][k].postToDB(url)
    # print "Client :" + str(i) + " of "+ str(len(data[1]))
    i+=1
if __name__ == '__main__' :

  mode = sys.argv[1]

  url = 'http://localhost:8080'

  requests_log = logging.getLogger("requests")
  requests_log.setLevel(logging.WARNING)
  logging.basicConfig(level=logging.WARNING)

  if mode == "Pickle":
    rootdir = sys.argv[2] if len(sys.argv) > 2 else '.'
    loadPickledData("pickled")
    loadData(rootdir)
    pickleData()
    print "Complete"
  elif mode=="Post":
    data = loadPickledData("pickled")
    # print(data)
    # loadData(rootdir)
    postToDB(url,data)


  else:
    print "Mode is either Pickle or Post"



  # postToDB(url)
