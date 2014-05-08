
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
import logging
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
	probedCount = ndb.ComputedProperty(lambda e: len(e.probedESSID))

	# TODO: Implement hardware API
	# hardware = ndb.JsonProperty()


	# NOTE: all class methods pass the instance of the class as it's first argument
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
	def queryNodesByBSSID(cls,bssid):
		nodesWIthESSID = []
		nodeRecordsQuery =  cls.query(cls.BSSID == bssid)
		device_records = nodeRecordsQuery.fetch()
		# print device_records
		return serialize(device_records)


	@classmethod
	def updateNode(cls,updateData):
		returnString = ""

		nodeRecordsQuery = cls.query(
			ancestor = device_key(updateData['bssid']))
		nodeToUpdate  = nodeRecordsQuery.get()
		return nodeToUpdate


	@classmethod
	def queryNodesByTimestamps(cls,device_name):
			device_readings_dict = {}
			nodeRecordsQuery = cls.query(
			ancestor = device_key(device_name)).order(-NodeRecord.timeRanges)

			device_records = nodeRecordsQuery.fetch()

			return device_records

	@classmethod
	def queryNodesByLastSeen(cls,queryTime):
			queryDTObj = 0

			queryDTObj = datetime.strptime(queryTime, "%Y-%m-%d %H:%M:%S")

			nodeRecordsQuery = cls.query(cls.lastSeen > queryDTObj).order(NodeRecord.lastSeen)
			device_records = nodeRecordsQuery.fetch()

			#for debug
			# logDict  = dict()
			# logDict[device.BSSID] = device.lastSeen
			# pprint(sorted(logDict.items(), key=lambda p: p[1], reverse=True))
			nodeJSONArray = []
			for device in device_records:
				nodeJSONArray.append(serialize(device))

			return nodeJSONArray

	@classmethod
	def queryNodesProbedESSID(cls, qrySSID):
			probedESSIDList = []
			nodeRecordsQuery = cls.query(cls.probedESSID.IN([qrySSID]))

			device_records = nodeRecordsQuery.fetch()

			nodeJSONArray = []
			for device in device_records:
				nodeJSONArray.append(serialize(device))

			return nodeJSONArray

	@classmethod
	def queryNodesbyNumProbedESSID(cls, num):
		probedESSIDList = []
		nodeRecordsQuery = cls.query(cls.probedCount  >= int(num))
		# print "Min num network requested" + num

		device_records = nodeRecordsQuery.fetch()
		# print device_records
		nodeJSONArray = []
		for device in device_records:
			nodeJSONArray.append(serialize(device))

		return nodeJSONArray

			# return device_records

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

		if kind == "Router":
			r = NodeRecord(parent = device_key(bssid),
						kind = kind, BSSID = bssid, timeRanges = curTimes , lastSeen = curTimes[-1], power = power, ESSID  = essid, probedESSID =probedEssid)
		else:
			r = NodeRecord(parent = device_key(bssid),
						kind = kind, BSSID = bssid, timeRanges = curTimes , lastSeen = curTimes[-1], power = power, AP = essid, probedESSID =probedEssid)

		r_key = r.put()

class UpdateRecordHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    update = dict()
    curTimes = []
    probedEssid = []
    try:
      self.response.headers['Content-Type'] = 'text/plain'

      update['kind'] = self.request.GET['kind'].strip()
      update['bssid'] = self.request.GET['bssid'].strip()
      update['power'] =  self.request.GET['power'].strip()
      update['essid'] =  self.request.GET['essid'].strip()
      probe = self.request.get_all('probed')
      timeRanges = self.request.get_all('times')


      for probed in probe:
        probed.encode('ascii','ignore')
        probed  = probed.strip()
        probedEssid.append(probed)

      update['probed'] = probedEssid

      for time in timeRanges:
        time.encode('ascii','ignore')
        time = time.strip()
        curTimes.append(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") )

    except KeyError: #bail if there is no argument for 'devicename' submitted
      self.response.write ('Error with update parameters')

    else:

      nodeToUpdate = NodeRecord.updateNode(update)
      nodeToUpdate.power = int(update['power'])
      nodeToUpdate.lastSeen = curTimes[-1]

      # NOTE: Commenting out this because it seems redundant to strore ranges for the real time app.
      #       Can always put it back for data analyis
      # nodeToUpdate.timeRanges = []
      # for t in update['time']:
      # nodeToUpdate.timeRanges.append(t)

      if nodeToUpdate.kind == "Client":
        nodeToUpdate.AP = update['essid']

      r_key = nodeToUpdate.put()
      self.response.write("Updated")

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
			bssid= self.request.GET['bssid']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			byBSSID = NodeRecord.queryNodesByBSSID(bssid)
			self.response.out.write("%s(%s)" %
                              (urllib2.unquote(self.request.get('callback')),
                               byBSSID))
			# self.response.write(


class ReadRecordsHandlerWithProbedESSID(webapp2.RequestHandler):

  def get(self):

    this = self
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.response.headers['Content-Type'] = 'application/javascript'
    # this.response.headers['Content-Type'] = 'text/plain'

    try:
      essid= self.request.GET['essid']

    except KeyError: #bail if there is no argument for 'devicename' submitted
      self.response.write ('NO DEVICE PARAMETER SUBMITTED')
    else:
      probed = NodeRecord.queryNodesProbedESSID(essid)
      self.response.out.write("%s(%s)" %
                              (urllib2.unquote(self.request.get('callback')),
                               probed))
      # self.response.write(
      #   NodeRecord.queryNodesProbedESSID(essid))

class ReadRecordsHandlerWithClientBSSID(webapp2.RequestHandler):

	def get(self):

		this = self
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers['Content-Type'] = 'application/javascript'
		# this.response.headers['Content-Type'] = 'text/plain'

		try:
			bssid= self.request.GET['bssid']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			# NodeRecord.queryNodesProbedESSID(essid))
			NodeRecord.queryNodesByBSSID(bssid))

	def post(self):
		self.response.write('<html><body>You wrote:<pre>')
		self.response.write(cgi.escape(self.request.get('content')))
		self.response.write('</pre></body></html>')

class ReadRecordsHandlerWithClients(webapp2.RequestHandler):
	def get(self):

		this = self
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers['Content-Type'] = 'application/javascript'
		# this.response.headers['Content-Type'] = 'text/plain'

		try:
			numNetworks= self.request.GET['minNetworks']
			# print "IM HERE" + numNetworks
		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			# self.response.write(
		  # NodeRecord.queryNodesProbedESSID(essid))
		# NodeRecord.queryNodesbyNumProbedESSID(numNetworks))
			clients =NodeRecord.queryNodesbyNumProbedESSID(numNetworks)
			self.response.out.write("%s(%s)" %
                              (urllib2.unquote(self.request.get('callback')),
                               clients))


	def post(self):
		self.response.write('<html><body>You wrote:<pre>')
		self.response.write(cgi.escape(self.request.get('content')))
		self.response.write('</pre></body></html>')

class LastSeenRecordsHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers['Content-Type'] = 'application/javascript'
		try:
			lastSeen= self.request.GET['lastseen']
			# print lastSeen

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			byLastSeen = NodeRecord.queryNodesByLastSeen(lastSeen)
			self.response.out.write("%s(%s)" %
                              (urllib2.unquote(self.request.get('callback')),
                               byLastSeen))




app = webapp2.WSGIApplication([
	webapp2.Route('/', handler = MainHandler, name = 'home'),

	webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-node'),
	webapp2.Route('/update', handler =  UpdateRecordHandler, name = 'update-node'),
	webapp2.Route('/byid', handler = ReadRecordsHandler, name = 'by-id'),
	webapp2.Route('/routeressid', handler = ReadRecordsHandlerWithESSID, name = 'router-by-essid'),
	webapp2.Route('/client', handler = ReadRecordsHandlerWithClientBSSID, name = 'client-by-essid'),
  webapp2.Route('/clients', handler = ReadRecordsHandlerWithClients, name = 'client-by-num'),
  webapp2.Route('/probed', handler = ReadRecordsHandlerWithProbedESSID, name = 'client-by-probed'),
	webapp2.Route('/deleteall', handler = DeleteAllRecordsHandler, name = 'delete-all'),
	webapp2.Route('/lastseen', handler = LastSeenRecordsHandler, name = 'last-seen')
	# webapp2.Route('/lastseenjs', handler = LastSeenJSRecordsHandler, name = 'last-seen-js'),



	# webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')

], debug=True)
