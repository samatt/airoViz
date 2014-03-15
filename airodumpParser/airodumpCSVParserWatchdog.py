from Node import Node
import sys
from oscSender import oscSender
import time, threading
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


def isAliveAndTimeChanged(kind,ID,lastTime):
	if kind == "Router":
		
		if ID not in routers:
			return False

		if not routers[ID].hasTimeChanged(lastTime):
			return False
		# if routers[ID].alive:
			# return False		
		return True

	else:
		if ID not in clients:
			return False

		if not clients[ID].hasTimeChanged(lastTime):
			return False
		# if clients[ID].alive:
			# return False		
		return True

def updateCurrentNode(kind,ID,lastTime,params):
	if kind == "Router":
	
		routers[ID].updateRouterNode(params)	
		sender.updateNode(routers[ID].wrapForOsc(),ID,"Router")
		routerIdleCount[ID] = 0
	
	else:
		clients[ID].updateClientNode(params)
		sender.updateNode(clients[ID].wrapForOsc(), ID, "Client")
		clientIdleCount[ID] = 0

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
			
			if isAliveAndTimeChanged("Router",ID,lastTime):
			
				updateCurrentNode("Router",ID,lastTime,params)
			
			elif ID in routers:
			
				updateIdleCount("Router",ID)
			
			else:
				addNewNode("Router",ID, params)

		else:
			# print isAliveAndTimeChanged("Client",ID,lastTime)
			if isAliveAndTimeChanged("Client",ID,lastTime):
			
				updateCurrentNode("Client",ID,lastTime,params)
			
			elif ID in clients:
			
				updateIdleCount("Client",ID)
			
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


class MyHandler(LoggingEventHandler):

    def on_modified(self, event):
    	if not event.is_directory:
			print event.src_path

			if ".kismet.csv" not in event.src_path and "kismet.netxml" not in event.src_path and ".cap" not in event.src_path:
				csv = open(event.src_path, 'r')
				readFile(csv)
				csv.close()		
				print "Reading File!"
				print event.src_path
			else:
				print "Ignoring file : "+event.src_path 


if __name__ == '__main__' :

   	event_handler = MyHandler()
   	path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()	
	
	sender = oscSender(8000)
	
	try :
	    while True :
			time.sleep(1)

	except KeyboardInterrupt :
		observer.stop()
		observer.join()
		print "Done"

