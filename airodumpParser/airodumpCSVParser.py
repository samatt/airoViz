from Node import Node
import sys
from oscSender import oscSender
import time, threading
routers = dict()
clients = dict()

routerBSSID = dict()
# newrouter
clientBSSID = dict()

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

def readFile(fileName):

	for line in fileName:
	
		line.strip()
		line = line.replace("\r\n"," ")
		params = line.split(',')

		if len(params) <6 :
			continue
		
		if params[0] == "BSSID":

			isRouter = True
			continue
		
		if params[0] == "Station MAC":

			isRouter = False
			continue 

		# if isRouter:
		# 	print "ROUTER: "
		# else:
		# 	print "CLIENT: "
		# print params
		params[2] = params[2].strip()
		params[0] = params[0].strip()
		
		if params[0] in routers and isRouter:
			if  routers[params[0]].alive:
				#collect ID (key) of all exisiting routers
				
				# print  "HERE"
				if routers[params[0]].hasTimeChanged(params[2]):
					# print param
					# print "Router " +  routers[params[0]].BSSID + " updated"
					routers[params[0]].updateRouterNode(params)	
					sender.updateNode(routers[params[0]].wrapForOsc(),params[0],"Router")
					routerBSSID[params[0]] = 0
				else:
					if params[0] in routerBSSID:
						routerBSSID[params[0]] += 1
					else:
						print 'wtf?'
			else:
				if routers[params[0]].hasTimeChanged(params[2]):
					routers[params[0]].updateRouterNode(params)
					# doing new node as it was previously 'dead' and that message was sent to the oF app
					sender.newNode(routers[params[0]].wrapForOsc(), params[0], "Router")		
		
		elif params[0] in clients and not isRouter:
			if clients[params[0]].alive:


				if clients[params[0]].hasTimeChanged(params[2]):

					# print  "Client " + clients[params[0]] .BSSID+ " updated"
				 	clients[params[0]].updateClientNode(params)
					sender.updateNode(clients[params[0]].wrapForOsc(), params[0], "Client")
					clientBSSID[params[0]] = 0
				else:
					if params[0] in clientBSSID:
						clientBSSID[params[0]] += 1
					else:
						print 'wtf?'
			else:
				if clients[params[0]].hasTimeChanged(params[2]):
					clients[params[0]].updateClientNode(params)
					# doing new node as it was previously 'dead' and that message was sent to the oF app
					sender.newNode(clients[params[0]].wrapForOsc(), params[0], "Client")

		else:
			if isRouter:
				n =  parseLine(params,isRouter)
				routers[n.BSSID] = n
				# routerBSSID.append(params[0])
				# print routers.keys()
				# print "adding routers" 
				routerBSSID[params[0]] = 1
				sender.newNode(n.wrapForOsc(),n.BSSID,"Router")
			else:
				n =  parseLine(params,isRouter)
				clients[n.BSSID] = n
				clientBSSID[params[0]] = 1
				sender.newNode(n.wrapForOsc(),n.BSSID,"Client")


def killNodes():
	#no longer deleteing the nodes, just turning them off for oF. input file never deletes so hard to tell when to stop
 	# print len(clientBSSID)  
 	# print len(routerBSSID) 
	print clientBSSID.values() 
	print "							"
	print  routerBSSID.values() 
	# print routers.keys()
	
	count = 10
	delClients = []
	delRouters = []

	for k, v in clientBSSID.iteritems():
	  if k in clientBSSID:
	  	if clientBSSID[k] > count:
		  	print "removeNode print" + k
			sender.removeNode(clients[k].wrapForOsc(),clients[k].BSSID,"Client")
			clientBSSID[k] = 0
			clients[k].alive = False
		# del clients[k]	  	

	for k, v in routerBSSID.iteritems():
	  if k in routerBSSID:
	  	if routerBSSID[k] > count:
		  	print "removeRouter " + k
			sender.removeNode(routers[k].wrapForOsc(),routers[k].BSSID,"Router")
			routerBSSID[k] = 0
			routers[k].alive = False

if __name__ == '__main__' :
	notFirsTime = False
	fileName = sys.argv[1]
	sender = oscSender(8000)
	try :
	    while 1 :

			time.sleep(1)
			
			print "test"

			csv = open(fileName, 'r')
			readFile(csv)
			if notFirsTime:
				killNodes()
			csv.close()
			notFirsTime = True


	except KeyboardInterrupt :
		    print "\nClosing OSCServer."
		    # mine.s.close()
		    # print "Waiting for Server-thread to finish"
		    # mine.st.join() ##!!!
		    print "Done"


		

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