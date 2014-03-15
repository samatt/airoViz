from Node import Node
import sys
import time, threading
import urllib2
import urllib
import requests
from datetime import datetime, date, time
import time
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

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
				routers[ID].updateDB()
			else:
				addNewNode("Router",ID, params)
				routers[ID].postToDB()


		else:
			if ID in clients:
				clients[ID].updateClientNode(params)
				clients[ID].updateDB()
			else:
				addNewNode("Client",ID,params)
				clients[ID].postToDB()

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
	i =0
	for k,v in routers.iteritems():

		routers[k].postToDB(url)
		print "Router :" + str(i) + " of "+ str(len(routers))
		i+=1
	
	i =0
	for k,v in clients.iteritems():
		clients[k].postToDB(url)	
		print "CLient :" + str(i) + " of "+ str(len(clients))
		i+=1

class MyHandler(LoggingEventHandler):

    def on_modified(self, event):
    	if not event.is_directory:
			print event.src_path

			if ".kismet.csv" not in event.src_path and "kismet.netxml" not in event.src_path and ".cap" not in event.src_path:
				csv = open(event.src_path, 'r')
				readFile(csv)
				csv.close()		
				# print "Reading File!"
				print event.src_path
			else:
				pass
				# print "Ignoring file : "+event.src_path 

if __name__ == '__main__' :
	
	url = 'http://localhost:8080'

   	event_handler = MyHandler()
   	path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()	

	# sender = oscSender(8000)

	try :
	    while True :
			time.sleep(1)

	except KeyboardInterrupt :
		observer.stop()
		observer.join()
		print "Done"
