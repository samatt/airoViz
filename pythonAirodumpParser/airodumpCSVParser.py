from Node import Node

import sys
if __name__ == '__main__' :
	fileName = sys.argv[1]
	csv = open(fileName, 'r')
	
	for line in csv:
		print line

	test = ['EC:55:F9:5A:3B:F2', '2014-02-24 18:52:20', '2014-02-24 19:02:54',  '1',  '54', 'WPA' , 'TKIP','PSK', '-93','1','0','0','0','0','0','9', 'U10C022FC']
	node1 = Node("Router",test);
	node1.printParams()
	node1 = Node(test);
	node1.printParams()
	test2 = [' 54:26:96:D5:44:A5 ', '2014-02-24 18:50:26', '                        2014-02-24 18:50:26				', '-81','5',' (not associated)' , 'nyu,belkin.48e','232CAFE','Au Bon Pain','nyupda']
	node2 = Node("Client",test2)
	node2.trimParams()
	node2.printParams()

	# test2 = list()