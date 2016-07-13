#UPDATE:
If you came here after watching my airoViz video on vimeo the viz code is here:
https://github.com/samatt/NSHeyy-Viz/blob/master/nw/app/scripts/graph.js

#Overview
This repository contains code for a platform for Wi-Fi based location tracking. It has three main components

* Aircrack-ng on Linux
* Python airodump Parser
	* Sends OSC messages of parsed data
	* Writes data to Google App Engine DB
	* Files
		* airodumpCSVParser.py:
				* Reads file on timer
				* Kills old nodes
				* Sends osc messages
		* airodumpCSVParserWatchdog.py
			* Uses watchdog to monitor when file has changed. Only reads file on change.
			* Checks the last time seen, only send OSC update if time has changed.
		* airodumpToDataStore.py
			* Use this to send a lot of old data to the data store in one shot.
			* Works for both individual files and directories

		* airodumpDataStoreRealTime.py
			* Use this to send data to the data store in real time. 

		* Node.py

* Google app NDB Data Store

##Aircrack-ng
Aircrack-ng and a compatible router are used to monitor the Wi-Fi spectrum for activity. The activity is can be split into two categories

###Router
Routers (as expected) are the devices that act as access points for logging on to networks.
 Aircrack provides the following paramteres for routers:

 * Authentication
 * BSSID
 * Beacons
 * Channel
 * Cipher
 * ESSID
 * First time seen
 * ID-length
 * IV
 * Key
 * LAN IP
 * Last time seen
 * Power
 * Privacy
 * Speed

###Client

* BSSID
* First time seen
* Last time seen
* Packets
* Power
* Probed ESSIDs
* Station MAC

##Python Airodump Parser

##NDB Datastore

 - Kind
 - BSSID
 - Power
 - Speed
 - TimeRanges
 	Time Ranges that the Node has been seen
 - ESSID
 	- Router: For Routers this is the Name of the network associated with that Router.
 	- Client: For Clients this is the name of the network the client is currently connected to. If client is not connected to any router this will say 'not associated'
 - probedESSIDs
 	These are the beacons that are found for an unassociated client. Not valid for routers

##RaspberryPi Bring-up Guide
 - Download PwnPi 3.0 http://pwnpi.sourceforge.net/
 - Flash SD Card
 - Install python 
 	-  ```apt-get install python-dev python-setuptools python-rpi.gpio python-pip``` 
 - Install python modules
 	- ```pip install requests```
 	- ```pip install watchdog```
 	- ```pip install pyOSC```
