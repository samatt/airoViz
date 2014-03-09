from Node import Node
import sys
import time, threading
import urllib2
import urllib
import requests
from datetime import datetime, date, time

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
		sender.newNode(n.wrapForOsc(),n.BSSID,"Router")
	
	else:
			
		# print "add clients"
		n =  parseLine(params,False)
		clients[n.BSSID] = n
		clientIdleCount[ID] = 1
		sender.newNode(n.wrapForOsc(),n.BSSID,"Client")

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
			addNewNode("Router",ID, params)

		else:
			# print isAliveAndTimeChanged("Client",ID,lastTime)
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


# class MyHandler(LoggingEventHandler):

#     def on_modified(self, event):
#     	if not event.is_directory:
# 			print event.src_path

# 			if ".kismet.csv" not in event.src_path and "kismet.netxml" not in event.src_path and ".cap" not in event.src_path:
# 				csv = open(event.src_path, 'r')
# 				readFile(csv)
# 				# killNodes()
# 				csv.close()		
# 				print "Reading File!"
# 				print event.src_path
# 			else:
# 				print "Ignoring file : "+event.src_path 

 #    def on_created(self,event):
 #    	print "Created"
	# def on_deleted(self,event):
	# 	print "Deleted"


if __name__ == '__main__' :

   	path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
	url = 'http://localhost:8080'
	startTime = '2014-02-26 14:49:08'
	endTime =  '2014-02-26 14:49:18'

	payload =  { 'kind':'Client', 'bssid':'00::AA::BB::CC::DD::EE','times' : startTime, 'power' : 10, 'essid' : "My Wi-Fi",'probed' :('test1','test2') }
	# payload =  { 'devicename':'pyTest2'}
	r = requests.get("http://localhost:8080/write", params=payload)
	# print (r.url)
	print r.json()
	# res = urllib2.urlopen(req)
	# html = res.read()

	# print html
	try :
	    while True :

			time.sleep(1)
			# csv = open(path, 'r')
			# readFile(csv)
			# killNodes()
			# csv.close()

	except KeyboardInterrupt :
		print "Done"

