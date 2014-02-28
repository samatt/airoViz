from OSC import OSCClient, OSCMessage

class oscSender(object):

	def __init__(self,port):
		self.client = OSCClient()
		self.client.connect( ("localhost", port) )
		print "Started server on port : " + str(port)

	def newNode(self,args):
		self.client.send( OSCMessage("/new", str(args) ) )

	def updateNode(self,args):
		self.client.send( OSCMessage("/update/", args ) )

	def removeNode(self,args):
		self.client.send( OSCMessage("/remove/Router", args ) )

	def closeConnection(self):

		if(kind == "Router"):
			self.client.send( OSCMessage("/quit", args ) )
	
