from Node import Node
import sys
from oscSender import oscSender
import time, threading
routers = dict()
clients = dict()

routerIdleCount = dict()
# newrouter
clientIdleCount = dict()

isRouter = None
def parseLine(params,isRouter):		

		if isRouter:
			node = Node("Router",params)
			node.trimParams()
			# node.printParams()
			return node
			
		
		elif not isRouter:
			node = Node("Client",params)
			node.trimParams()
			# node.printParams()
			return node
			# pass
def isAliveAndTimeChanged(kind,ID,lastTime):
	if kind == "Router":
		
		if ID not in routers:
			return False

		if not routers[ID].hasTimeChanged(lastTime):
			return False

		if routers[ID].alive:
			return False		

		return True

	else:
		if ID not in clients:
			return False

		if not clients[ID].hasTimeChanged(lastTime):
			print "Time hasnt changed"
			return False

		if clients[ID].alive:
			return False		

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
		else:
			print 'wtf?'
	else:
		if ID in clientIdleCount:
			clientIdleCount[ID] += 1
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
		
		print "add clients"
		n =  parseLine(params,False)
		clients[n.BSSID] = n
		clientIdleCount[ID] = 1
		sender.newNode(n.wrapForOsc(),n.BSSID,"Client")

def readFile(fileName):

	for line in fileName:
	
		line.strip()
		line = line.replace("\r\n"," ")
		params = line.split(',')

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
	
	count = 40

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
			

if __name__ == '__main__' :

	fileName = sys.argv[1]
	sender = oscSender(8000)
	try :
	    while 1 :

			time.sleep(1)
			
			print "test"

			csv = open(fileName, 'r')
			readFile(csv)
			killNodes()
			csv.close()
			


	except KeyboardInterrupt :
		    print "\nClosing OSCServer."
		    # mine.s.close()
		    # print "Waiting for Server-thread to finish"
		    # mine.st.join() ##!!!
		    print "Done"


########OLD CODE
		# if ID in routers and isRouter:
		# 	if  routers[ID].alive:
		# 		#collect ID (key) of all exisiting routers
				
		# 		# print  "HERE"
		# 		if routers[ID].hasTimeChanged(lastTime):
		# 			# print param
		# 			# print "Router " +  routers[ID].BSSID + " updated"
		# 			routers[ID].updateRouterNode(params)	
		# 			sender.updateNode(routers[ID].wrapForOsc(),ID,"Router")
		# 			routerIdleCount[ID] = 0
		# 		else:
		# 			if ID in routerIdleCount:
		# 				routerIdleCount[ID] += 1
		# 			else:
		# 				print 'wtf?'
		# 	else:
		# 		if routers[ID].hasTimeChanged(lastTime):
		# 			routers[ID].updateRouterNode(params)
		# 			# doing new node as it was previously 'dead' and that message was sent to the oF app
		# 			sender.newNode(routers[ID].wrapForOsc(), ID, "Router")		
		
		# elif ID in clients and not isRouter:
		# 	if clients[ID].alive:


		# 		if clients[ID].hasTimeChanged(lastTime):

		# 			# print  "Client " + clients[ID] .BSSID+ " updated"
		# 		 	clients[ID].updateClientNode(params)
		# 			sender.updateNode(clients[ID].wrapForOsc(), ID, "Client")
		# 			clientIdleCount[ID] = 0
		# 		else:
		# 			if ID in clientIdleCount:
		# 				clientIdleCount[ID] += 1
		# 			else:
		# 				print 'wtf?'
		# 	else:
		# 		if clients[ID].hasTimeChanged(lastTime):
		# 			clients[ID].updateClientNode(params)
		# 			# doing new node as it was previously 'dead' and that message was sent to the oF app
		# 			sender.newNode(clients[ID].wrapForOsc(), ID, "Client")

		# else:
			# if isRouter:
			# 	n =  parseLine(params,isRouter)
			# 	routers[n.BSSID] = n
			# 	# routerIdleCount.append(ID)
			# 	# print routers.keys()
			# 	print "add routers" 
			# 	routerIdleCount[ID] = 1
			# 	sender.newNode(n.wrapForOsc(),n.BSSID,"Router")
			# else:
			# 	print "add clients"
			# 	n =  parseLine(params,isRouter)
			# 	clients[n.BSSID] = n
			# 	clientIdleCount[ID] = 1
			# 	sender.newNode(n.wrapForOsc(),n.BSSID,"Client")
#########		

	# test = ['EC:55:F9:5A:3B:F2', '2014-02-24 18:52:20', '2014-02-24 19:02:54',  '1',  '54', 'WPA' , 'TKIP','PSK', '-93','1','0','0','0','0','0','9', 'U10C022FC']
	# node1 = Node("Router",test);
	# node1.printParams()
	# node1 = Node(test);
	# node1.printParams()
	# test2 = [' 54:26:96:D5:44:A5 ', '2014-02-24 18:50:26', '                        2014-02-24 18:50:26				', '-81','5',' (not associated)' , 'nyu,belkin.48e','232CAFE','Au Bon Pain','nyupda']
	# node2 = Node("Client",test2)
	# node2.trimParams()
	# node2.printParams()

	# test2 = list()