

function setDuration (numHours, numMinutes, numSeconds){

	var ts = new Date();

	var minutes = (ts.getMinutes()-numMinutes) >0 ? (ts.getMinutes()-numMinutes) : 0
	var seconds = (ts.getSeconds()-numSeconds) >0 ? (ts.getSeconds()-numSeconds) : 0
	var hours 	= (ts.getHours()-numHours) >0 ? (ts.getHours()-numHours) : 0

	//FIXME: Get rid off the -1 from getDate
	timestamp = ts.getFullYear()+"-"+(ts.getMonth()+1)+"-"+(ts.getDate()-1)+" "+hours+":"+ minutes	+":"+seconds;
	return timestamp
}
