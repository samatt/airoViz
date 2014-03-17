
import urllib
import webapp2
# try: import simplejson as json
# except ImportError: import  json
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from urlparse import urlparse, parse_qs
from datetime import datetime, date, time
from pprint import pprint
import urllib2
# from dateutil import parser


class GaeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime('%Y-%m-%d %H:%M:%S'))
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)

def serialize(object_to_serialize):
    return json.dumps(object_to_serialize, cls=GaeEncoder)

NO_DEVICE_ID = 'no_device_id'        
def device_key(device_name = NO_DEVICE_ID):
	"""constructs Datastore key for NodeRecord entity with device_name """
	return ndb.Key('NodeGroup', device_name)

class NodeRecord(ndb.Expando) :
	"""Models a node found by airodump-ng. It contains kind, BSSID, first and last time seen, Channel, Speed, Privacy, Power, IP, ESSID, probedESSID"""
	kind = ndb.StringProperty()
	BSSID = ndb.StringProperty()
	# This is going to be a list of time ranges the device was seen.

	##EVEN INDICES ARE START TIMES AND ODD ARE LAST SEEN
	power= ndb.IntegerProperty()
	ESSID = ndb.StringProperty(default = "None")
	# associatedAP  = ndb.JSONProperty(default = "None")
	Privacy = ndb.StringProperty(default = "None")
	probedESSID = ndb.StringProperty(repeated = True) 

	AP = ndb.StringProperty(default = "None")
	timeRanges = ndb.DateTimeProperty(repeated = True)
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)
	lastSeen = ndb.DateTimeProperty()
	
	# TODO: Implement hardware API
	# hardware = ndb.JsonProperty()


	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def queryByNode(cls,device_name):
			device_readings_list = []
			nodeRecordsQuery = cls.query(
			ancestor = device_key(device_name)).order(-NodeRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
			device_records = nodeRecordsQuery.fetch()

		#create methods for pulling different streams of data out for processing. 
			# for device_record in device_records:
				# device_readings_list.append(device_record.sensorreading)
			return device_records

	@classmethod
	def queryNodesByESSID(cls,essid):
		nodesWIthESSID = []
		nodeRecordsQuery =  cls.query(cls.ESSID == essid)
		device_records = nodeRecordsQuery.fetch()

		return device_records


	@classmethod
	def updateNode(cls,updateData):
		returnString = "" 

		nodeRecordsQuery = cls.query(
			ancestor = device_key(updateData['bssid']))

		##using get as we only want the first query (only one entity should exist)
		nodeToUpdate  = nodeRecordsQuery.get()
		# print "\n##################################\n"
		# print nodeToUpdate
		# print "\n##################################\n"
		return nodeToUpdate
		# if nodeToUpdate.kind == "Router":
		# 	returnString += "Router "+ nodeToUpdate.BSSID + "\n "
		# 	returnString += str(nodeToUpdate.power) + " updated to " + str(updateData['power'])+ "\n"
		# 	returnString += "Last Time updated seen : " + str(updateData['time']) + "  \n"

		# 	nodeToUpdate.power = int(updateData['power'])
		# 	nodeToUpdate.timeRanges = updateData['time']

		# else:
		# 	returnString += "Client "+ nodeToUpdate.BSSID + "\n "
		# 	returnString += "Power : "+ str(nodeToUpdate.power) + " updated to " + str(updateData['power'])+ "\n"
		# 	returnString += "Last Time : updated to " + str(updateData['time']) + "  \n"
		# 	returnString += "AP : "+ nodeToUpdate.AP + " updated to " + updateData['essid'] + "\n"

		# 	nodeToUpdate.power = int(updateData['power'])
		# 	nodeToUpdate.timeRanges = updateData['time']
		# 	nodeToUpdate.AP = updateData['essid']
		

	@classmethod
	def queryNodesByTimestamps(cls,device_name):
			device_readings_dict = {}
			nodeRecordsQuery = cls.query(
			ancestor = device_key(device_name)).order(-NodeRecord.timeRanges)
			
			device_records = nodeRecordsQuery.fetch()
			
			return device_records

	@classmethod
	def queryNodesByLastSeen(cls,queryTime,fromJS):
			queryDTObj = 0
			if fromJS:
				queryTime = float(queryTime)
				queryDTObj = datetime.fromtimestamp(queryTime/1000)

				print "##################"
				print queryDTObj
				print queryDTObj.second
				print queryDTObj.microsecond
				print "##################"				
			else:
				queryDTObj = datetime.strptime(queryTime, "%Y-%m-%d %H:%M:%S")
			
			nodeRecordsQuery = cls.query(cls.lastSeen > queryDTObj).order(NodeRecord.lastSeen)
			
			device_records = nodeRecordsQuery.fetch()
			# JSONEncoder().encode( nodeRecordsQuery.fetch())
			logDict  = dict()
			nodeJSONArray = []
			for device in device_records:
				logDict[device.BSSID] = device.lastSeen
				nodeJSONArray.append(serialize(device))
			pprint(sorted(logDict.items(), key=lambda p: p[1], reverse=True))

			return nodeJSONArray			

	@classmethod
	def queryNodesProbedESSID(cls, qrySSID):
			probedESSIDList = []
			nodeRecordsQuery = cls.query( cls.probedESSID.IN([qrySSID]))	
			
			device_records = nodeRecordsQuery.fetch()

			return device_records

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('hello world')

class CreateRecordHandler(webapp2.RequestHandler):
    
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		kind = self.request.GET['kind'].strip()
		bssid = self.request.GET['bssid'].strip()
		probe = self.request.get_all('probed')
		power =  self.request.GET['power'].strip()
		essid =  self.request.GET['essid'].strip()
		timeRanges = self.request.get_all('times')
		curTimes = []
		probedEssid = []
		
		for probed in probe:
			probed.encode('ascii','ignore')
			probed  = probed.strip()
			probedEssid.append(probed)

		for time in timeRanges:
			time.encode('ascii','ignore')
			time = time.strip()
			curTimes.append(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") )
		
		power = int(power)
		print power

		if kind == "Router":
			r = NodeRecord(parent = device_key(bssid),
						kind = kind, BSSID = bssid, timeRanges = curTimes , lastSeen = curTimes[-1], power = power, ESSID  = essid, probedESSID =probedEssid)
		else:
			r = NodeRecord(parent = device_key(bssid),
						kind = kind, BSSID = bssid, timeRanges = curTimes , lastSeen = curTimes[-1], power = power, AP = essid, probedESSID =probedEssid)

		r_key = r.put()

class ReadRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['bssid']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			NodeRecord.queryByNode(device_name))

class DeleteAllRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		node_keys = NodeRecord.query().fetch(keys_only=True)
		ndb.delete_multi(node_keys)

class ReadRecordsHandlerWithESSID(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			essid= self.request.GET['essid']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			NodeRecord.queryNodesByESSID(essid))

class ReadRecordsHandlerWithClientESSID(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			essid= self.request.GET['essid']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			NodeRecord.queryNodesProbedESSID(essid))			

class ReadLatestRecordHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:

			reading = NodeRecord.query_latest_reading(device_name)

			#self.response.write(decoded_dict.get('devicename') + '\n')
			#self.response.write(decoded_dict.get('a0'))

			self.response.write(reading)

		
			 #outputs key value dictionary of retrieved datastore entity. 
	
class LastSeenRecordsHandler(webapp2.RequestHandler):
	def get(self):
		# self.response.headers['Content-Type'] = 'text/plain'
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers['Content-Type'] = 'application/javascript'
		try:
			lastSeen= self.request.GET['lastseen']


		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			byLastSeen = NodeRecord.queryNodesByLastSeen(lastSeen,False)
			self.response.out.write("%s(%s)" %
                              (urllib2.unquote(self.request.get('callback')),
                               byLastSeen))			
			# self.response.write(byLastSeen)

class LastSeenJSRecordsHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		try:
			jsTimeStamp= self.request.GET['lastseen']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			byLastSeen = NodeRecord.queryNodesByLastSeen(jsTimeStamp,False)
			# decoded_dict = dict(json.loads(reading))
			self.response.write(byLastSeen)

class UpdateRecordHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		update = dict()
		try:
			self.response.headers['Content-Type'] = 'text/plain'
			
			update['kind'] = self.request.GET['kind'].strip()
			update['bssid'] = self.request.GET['bssid'].strip()
			update['power'] =  self.request.GET['power'].strip()
			update['essid'] =  self.request.GET['essid'].strip()


			probe = self.request.get_all('probed')
			timeRanges = self.request.get_all('times')
			curTimes = []
			probedEssid = []
			
			for probed in probe:
				probed.encode('ascii','ignore')
				probed  = probed.strip()
				probedEssid.append(probed)

			update['probed'] = probedEssid

			for time in timeRanges:
				time.encode('ascii','ignore')
				time = time.strip()
				curTimes.append(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") )

			update['time'] = curTimes

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('Error with update parameters')
		
		else:
			nodeToUpdate = NodeRecord.updateNode(update)
			# returnString = ""
			if nodeToUpdate.kind == "Router":
				print "Router "+ nodeToUpdate.BSSID + "\n "
				print str(nodeToUpdate.power) + " updated to " + str(update['power'])+ "\n"
				print "Last Time updated seen : " + str(update['time']) + "  \n"

				nodeToUpdate.power = int(update['power'])
				nodeToUpdate.lastSeen = update['time'][-1]
				for t in update['time']:
					nodeToUpdate.timeRanges.append(t)	

				

			else:
				print "Client "+ nodeToUpdate.BSSID + "\n "
				print "Power : "+ str(nodeToUpdate.power) + " updated to " + str(update['power'])+ "\n"
				print "Last Time : updated to " + str(update['time']) + "  \n"
				print "AP : "+ nodeToUpdate.AP + " updated to " + update['essid'] + "\n"

				nodeToUpdate.power = int(update['power'])
				#Doing this because it seems redundant to strore ranges for the real time app. Can always put it back for data analyis

				nodeToUpdate.lastSeen = update['time'][-1]
				nodeToUpdate.timeRanges = []
				for t in update['time']:
					nodeToUpdate.timeRanges.append(t)	
				# nodeToUpdate.timeRanges.append(update['time'])
				
				nodeToUpdate.AP = update['essid']			
			# decoded_dict = dict(json.loads(reading))
			print
			r_key = nodeToUpdate.put()
			self.response.write("Updated")

class CORSEnabledHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers.add_header("Access-Control-Allow-Origin", "*")
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.out.write(self.dump_csv())


app = webapp2.WSGIApplication([
	webapp2.Route('/', handler = MainHandler, name = 'home'),
	# webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-record'),
	# webapp2.Route('/read', handler = ReadRecordsHandler, name = 'read-values'),
	# webapp2.Route('/read-time', handler = ReadRecordsHandlerWithTime, name = 'read-values-with-time'),
	# webapp2.Route('/read-latest', handler = ReadLatestRecordHandler, name = 'read-latest-value'),
	# webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')

	webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-node'),
	webapp2.Route('/update', handler =  UpdateRecordHandler, name = 'update-node'),
	webapp2.Route('/byid', handler = ReadRecordsHandler, name = 'by-id'),
	webapp2.Route('/routeressid', handler = ReadRecordsHandlerWithESSID, name = 'router-by-essid'),
	webapp2.Route('/clientessid', handler = ReadRecordsHandlerWithClientESSID, name = 'client-by-essid'),
	webapp2.Route(	'/deleteall', handler = DeleteAllRecordsHandler, name = 'delete-all'),
	webapp2.Route('/lastseen', handler = LastSeenRecordsHandler, name = 'last-seen'),
	webapp2.Route('/lastseenjs', handler = LastSeenJSRecordsHandler, name = 'last-seen-js'),



	# webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')

], debug=True)


 