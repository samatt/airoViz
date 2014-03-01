from OSC import OSCClient, OSCMessage

class oscSender(object):

	def __init__(self,port):
		self.client = OSCClient()
		self.client.connect( ("localhost", port) )
		print "Started server on port : " + str(port)

	def newNode(self,args,BSSID,kind):
		msg = OSCMessage("/new" )
		msg.append(kind.strip())
		msg.append(args)
		msg.append(BSSID.strip()) 
		self.client.send(msg)
		# print "new"

	def updateNode(self,args,BSSID,kind):
		msg =  OSCMessage("/update")
		msg.append(kind.strip())
		msg.append(args)
		msg.append(BSSID.strip()) 
		self.client.send(msg)
		# print "update"

	def removeNode(self,args,BSSID, kind):
		msg =  OSCMessage("/remove")
		msg.append(kind.strip())
		msg.append(args)
		msg.append(BSSID.strip())  
		self.client.send(msg)

	def closeConnection(self):
		self.client.send( OSCMessage("/quit", args ) )
	
