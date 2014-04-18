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


def postToDB(url):
  i =0
  for k,v in routers.iteritems():

    routers[k].postToDB(url)
    print "Router :" + str(i) + " of "+ str(len(routers))
    i+=1

  i =0
  for k,v in clients.iteritems():
    clients[k].postToDB(url)
    print "Client :" + str(i) + " of "+ str(len(clients))
    i+=1

  pickle.dump(routers, open( "routers.p", "wb" ) )
  pickle.dump(clients, open( "client.p", "wb" ) )
if __name__ == '__main__' :
  requests_log = logging.getLogger("requests")
  requests_log.setLevel(logging.WARNING)

  logging.basicConfig(level=logging.DEBUG)
   # 	path = sys.argv[1] if len(sys.argv) > 1 else '.'
  rootdir = sys.argv[1] if len(sys.argv) > 1 else '.'

  # print rootdir
  url = 'http://localhost:8080'
  # url = "http://direct-electron-537.appspot.com/"
  # csv = open(path, 'r')
  # readFile(csv)
  # csv.close()
  # postToDB(url)
  #
  # print "Done"
  i =0
  for subdir, dirs, files in os.walk(rootdir):
    size = len(routers)
    sizeC = len(clients)
    for file in files:

      # print subdir+'/'+file
      if ".kismet.csv" not in file and "kismet.netxml" not in file and ".cap" not in file and ".csv" in file:
        csv = open(subdir+"/"+file, 'r')
        print "Reading File :" + file

        readFile(csv)
      # killNodes()
        csv.close()
        postToDB(url)

        print
      else:
        print "Ignoring file : "+file


  # 		print "### " + str(i) + " of "+ str(len(files))
  # 		print " No of routers added : "+ str(len(routers) - size)
  # 		print " No of clients added : "  + str(len(clients) - sizeC)
  # 		print " No of routers total  : "	+ len(routers)
  # 		print " No of clients total  : "	+ len(clients)
  # 		i += 1

  # postToDB(url)
