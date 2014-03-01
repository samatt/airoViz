from Node import Node
import sys
from oscSender import oscSender
import time, threading
routers = dict()
clients = dict()

routerBSSID = []
# newrouter
clientBSSID = []

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
			#collect ID (key) of all exisiting routers
			routerBSSID.append(params[0])	
			# print  "HERE"
			if routers[params[0]].hasTimeChanged(params[2]):
				# print param
				# print "Router " +  routers[params[0]].BSSID + " updated"
				routers[params[0]].updateRouterNode(params)	
				sender.updateNode(routers[params[0]].wrapForOsc(),params[0],"Router")
				
		
		elif params[0] in clients and not isRouter:

			#collect ID (key) of all exisiting clients
			clientBSSID.append(params[0])
			# print clientBSSID
			# print  "THERE"

			if clients[params[0]].hasTimeChanged(params[2]):

				# print  "Client " + clients[params[0]] .BSSID+ " updated"
			 	clients[params[0]].updateClientNode(params)
				sender.updateNode(clients[params[0]].wrapForOsc(), params[0], "Client")		
				
				

		else:
			if isRouter:
				n =  parseLine(params,isRouter)
				routers[n.BSSID] = n
				routerBSSID.append(params[0])
				# print routers.keys()
				print "adding routers" 
				sender.newNode(n.wrapForOsc(),n.BSSID,"Router")
			else:
				n =  parseLine(params,isRouter)
				clients[n.BSSID] = n
				clientBSSID.append(params[0])
				sender.newNode(n.wrapForOsc(),n.BSSID,"Client")


def deleteDeadNodes():
	
 	print len(clientBSSID)  
 	print len(routerBSSID) 
	print clientBSSID 
	print clients.keys()
	print  routerBSSID 
	print routers.keys()
	
	clientsCopy = clients;
	routersCopy = routers;
	delClients = []
	delRouters = []

	for k, v in clientsCopy.iteritems():
	  if k not in clientBSSID:
	  	print "removeNode " + k
		sender.removeNode(clients[k].wrapForOsc(),clients[k].BSSID,"Client")
		delClients.append(k)
		# del clients[k]	  	

	for k, v in routersCopy.iteritems():
	  if k not in routerBSSID:
	  	print "removeClient " + k
		sender.removeNode(routers[k].wrapForOsc(),routers[k].BSSID,"Router")
		delRouters.append(k)
		# del routers[k]	  			

	
	for k in delClients:
		del clients[k]
	
	for k in delRouters:
		del routers[k]		
	# for i in clientBSSID:
	# 	if i in clients:
	# 		pass		
	# 	else:
	# 		# print "Removing Client ID: " +i
	# 		sender.removeNode(clients[i].wrapForOsc(),clients[i].BSSID,"Client")
	# 		del clients[i]

	# for i in routerBSSID:
	# 	if i in routers:
	# 		pass
	# 	else:
	# 		# print "Removing Router ID: " + i
	# 		sender.removeNode(routers[i].wrapForOsc(),routers[i].BSSID,"Router")
	# 		del routers[i]
		
	del routerBSSID [:]
	del clientBSSID [:]
	print len(clients)
	print len(routers)
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
				deleteDeadNodes()
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