
import urllib
import webapp2
try: import simplejson as json
except ImportError: import  json
from google.appengine.api import users
from google.appengine.ext import ndb
from urlparse import urlparse, parse_qs
from datetime import datetime, date, time
# from dateutil import parser

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
	timeRanges = ndb.DateTimeProperty(repeated = True)
	power= ndb.IntegerProperty()
	ESSID = ndb.StringProperty(default = "None")
	# associatedAP  = ndb.JSONProperty(default = "None")
	Privacy = ndb.StringProperty(default = "None")
	probedESSID = ndb.StringProperty(repeated = True) 
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)
	# TODO: Implement hardware API
	# hardware = ndb.JsonProperty()


	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def queryByNode(cls,device_name):
			device_readings_list = []
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-NodeRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
			device_records = device_records_query.fetch()

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
	def queryNodesByTimestamps(cls,device_name):
			device_readings_dict = {}
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-NodeRecord.timeRanges)
			
			device_records = device_records_query.fetch()
			
			return device_records

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
		probedEssid = self.request.get_all('probed')
		power =  self.request.GET['power'].strip()
		essid =  self.request.GET['essid'].strip()
		timeRanges = self.request.get_all('times')
		curTimes = []
		
		for probed in probedEssid:
			probed  = probed.strip()
			print probed
			probed.encode('ascii','ignore')
			print probed

		print timeRanges
		for time in timeRanges:
			time.encode('ascii','ignore')
			time = time.strip()
			curTimes.append(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") )
			print curTimes
		
		power = int(power)
		print power
		r = NodeRecord(parent = device_key(bssid),
						kind = kind, BSSID = bssid, timeRanges = curTimes , power = power, ESSID  = essid, probedESSID =probedEssid)
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

class UpdateRecordHandler(webapp2.RequestHandler):

	def get(self): 
		pass
		# this = self
		# this.response.headers['Content-Type'] = 'text/plain'
		
		# try:
		# 	device_name= self.request.GET['devicename']

		# except KeyError: #bail if there is no argument for 'devicename' submitted
		# 	self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		# else:
		# 	self.response.write(
		# 	NodeRecord.queryByNode(device_name))			

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

			reading = SensorRecord.query_latest_reading(device_name)

			#self.response.write(decoded_dict.get('devicename') + '\n')
			#self.response.write(decoded_dict.get('a0'))

			self.response.write(reading)

		
			 #outputs key value dictionary of retrieved datastore entity. 
	
class PassSensorValueOnly(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			reading = SensorRecord.query_latest_reading(device_name)
			decoded_dict = dict(json.loads(reading))
			self.response.write(decoded_dict.get('a0'))


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
	webapp2.Route('/clientessid', handler = ReadRecordsHandlerWithClientESSID, name = 'client-by-essid')
	# webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')

], debug=True)


 