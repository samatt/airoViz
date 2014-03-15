from Node import Node
import sys
import time, threading
import urllib2
import urllib
import requests
from datetime import datetime, date, time
import time
import os

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

def killNodes():

	#no longer deleteing the nodes, just turning them off for oF. input file never deletes so hard to tell when to stop
	print clientIdleCount.values()
	print routerIdleCount.values()
	count = 100

	for k, v in clientIdleCount.iteritems():
	  
	  if k in clientIdleCount:
	  
	  	if v > count:
	  
	  		if clients[k].alive == True:
	
			  	print "remove client" + k
				sender.removeNode(clients[k].wrapForOsc(),clients[k].BSSID,"Client")
				clientIdleCount[k] = 1
				clients[k].alive = False

	for k, v in routerIdleCount.iteritems():
	  
	  if k in routerIdleCount:
	  	
	  	if v > count:
		  	if routers[k].alive == True:
			  	print "remove router " + k
				sender.removeNode(routers[k].wrapForOsc(),routers[k].BSSID,"Router")
				routerIdleCount[k] = 1
				routers[k].alive = False

def postToDB(url):
	for k,v in routers.iteritems():

		routers[k].postToDB(url)
	
	for k,v in clients.iteritems():
		clients[k].postToDB(url)		


# def postToDB(url):
# 	for k,v in routers.iteritems():
# 		routers[k].postToDB(url)
if __name__ == '__main__' :

   	path = sys.argv[1] if len(sys.argv) > 1 else '.'
	rootdir = sys.argv[1] #if len(sys.argv) > 1 else '.'
	
	print rootdir
	url = 'http://localhost:8080'
	# csv = open(path, 'r')
	# readFile(csv)
	# csv.close()
	# postToDB(url)

	print "Done"
	i =0
	for subdir, dirs, files in os.walk(rootdir):
	    for file in files:

			# print subdir+'/'+file
			if ".kismet.csv" not in file and "kismet.netxml" not in file and ".cap" not in file:
				print "Reading File :" + file
				csv = open(subdir+'/'+file, 'r')
				readFile(csv)
			# killNodes()
				csv.close()		
				
				print 
			else:
				print "Ignoring file : "+file 

			print "### " + str(i) + " of "+ str(len(files))

			# print clients
			# print routers
			i += 1

	postToDB(url)

