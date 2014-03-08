#ndb_store
=========

ndb_store is a simple Google App Engine Application that allows one to save sensor data vi HTTP GET requests. 

The API has 2 routes at present 'write' for creating a datastore record and 'read' to recall saved sensor values. 

**To sumbit via '/write':**

-http://YOUR_APP_SPOT_URL_HERE/write?devicename=STRING&sensorreading=INT&sensormin=INT&sensormax=INT
 
 This will create a datastore entity whose parent is the device.  You can retrieve all of the sensors readings via 'read'
 
 To retrieve all of a sensors reading values:
 
 http://YOUR_APP_SPOT_URL_HERE/read?devicename=STRING
 
 For example you submit:
 
 -http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=244&sensormin=0&sensormax=1024
-http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=48&sensormin=0&sensormax=1024
-http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=67&sensormin=0&sensormax=1024
 -http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=5&sensormin=0&sensormax=1024
 
 **Then you retrieve via '/read'.**
 
 -http://YOUR_APP_SPOT_URL_HERE/read?devicename=bluto
 
 The server returns
 [5,67,48,244]
 
 or you can have it return a dictionary that has the creation timestamp as it's key
 
 -http://YOUR_APP_SPOT_URL_HERE/read-time?devicename=bluto
 
 The server returns
 {datetime.datetime(2014, 1, 24, 20, 16, 17, 559010): 5, datetime.datetime(2014, 1, 24, 20, 16, 38, 818940): 48, datetime.datetime(2014, 1, 24, 20, 15, 54, 543310): 22, datetime.datetime(2014, 1, 24, 20, 16, 10, 965960): 244, datetime.datetime(2014, 1, 24, 20, 16, 24, 399260): 67, datetime.datetime(2014, 1, 24, 20, 16, 1, 335910): 244}
 
 
 
 
