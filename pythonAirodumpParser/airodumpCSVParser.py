from Node import Node
import sys
# import OSC
import time, threading
nodes = dict()
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

		if len(params) <7 :
			continue
		# print params
		if(line < 2 ):
			continue
		
		if params[0] == "BSSID":

			isRouter = True
			continue
		
		if params[0] == "Station MAC":

			isRouter = False
			continue 
		
		if params[0] in nodes:	
			# print nodes[params[0]].hasTimeChanged(params[2])
			params[2] = params[2].strip()
			if nodes[params[0]].hasTimeChanged(params[2]):

				if isRouter:
					nodes[params[0]].updateRouterNode(params)
				elif not isRouter:
					nodes[params[0]].updateClientNode(params)
		else:
			n =  parseLine(params,isRouter)
			nodes[n.BSSID] = n

		# print len(nodes)
if __name__ == '__main__' :

	fileName = sys.argv[1]

	try :
	    while 1 :

			time.sleep(1)
			print "test"

			csv = open(fileName, 'r')

			readFile(csv)

			csv.close()


	except KeyboardInterrupt :
		    print "\nClosing OSCServer."
		    # mine.s.close()
		    print "Waiting for Server-thread to finish"
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