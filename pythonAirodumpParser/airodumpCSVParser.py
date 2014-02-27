from Node import Node
import sys

def parseLine(line,isRouter):		

		if isRouter:
			node = Node("Router",params)
			node.trimParams()
			node.printParams()
			# return
			pass
		
		elif not isRouter:
			node = Node("Client",params)
			node.trimParams()
			node.printParams()
			# return
			pass	


if __name__ == '__main__' :
	fileName = sys.argv[1]
	csv = open(fileName, 'r')
	isRouter = None
	
	for line in csv:
		
		line.strip()
		line = line.replace("\r\n"," ")
		params = line.split(',')

		if len(params) <2 :
			continue
		print params
		if(line < 2 ):
			continue
		
		if params[0] == "BSSID":

			isRouter = True
			continue
		
		if params[0] == "Station MAC":

			isRouter = False
			continue 
		
		parseLine(line,isRouter)


		

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