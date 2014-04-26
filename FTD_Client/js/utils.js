
app = new Object();
app.server = 'localhost:8080';
// app.server ='direct-electron-537.appspot.com';
app.nodes = [];
app.links = [];
app.refreshInterval = 10000;
var node = null;
var link = null;
var numBadges = 19;
function setDuration (numHours, numMinutes, numSeconds){

	var ts = new Date();

	var minutes = (ts.getMinutes()-numMinutes) >0 ? (ts.getMinutes()-numMinutes) : 0
	var seconds = (ts.getSeconds()-numSeconds) >0 ? (ts.getSeconds()-numSeconds) : 0
	var hours 	= (ts.getHours()-numHours) >0 ? (ts.getHours()-numHours) : 0

	//FIXME: Get rid off the -1 from getDate and -2 from hours
	timestamp = ts.getFullYear()+"-"+(ts.getMonth()+1)+"-"+(ts.getDate())+" "+(hours)+":"+ minutes	+":"+seconds;
	// timestamp = ts.getFullYear()+"-"+(ts.getMonth()+1)+"-"+(ts.getDate()-2)+" "+(13)+":"+ minutes	+":"+seconds;
	return timestamp
}

function getRandomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


var scale = d3.scale.pow()
	.domain([0,128])
	.range([10,3]);

var scale2 = d3.scale.linear()
	.domain([0,128])
	.range([1,0]);

var colors = d3.scale.category20();
var color = d3.scale.category10();
