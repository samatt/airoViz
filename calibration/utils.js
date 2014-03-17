function setDuration (numMinutes){
	var ts = new Date();
	// console.log( (ts.getMinutes()-numMinutes) >0 ? (ts.getMinutes()-numMinutes) : 0)
	minutes = (ts.getMinutes()-numMinutes) >0 ? (ts.getMinutes()-numMinutes) : 0
	// timestamp = ts.getUTCFullYear()+"-"+(ts.getUTCMonth()+1)+"-"+ts.getUTCDate()+" "+ts.getUTCHours()+":"+ minutes	+":"+ts.getUTCSeconds();
	timestamp = ts.getFullYear()+"-"+(ts.getMonth()+1)+"-"+ts.getDate()+" "+ts.getHours()+":"+ minutes	+":"+ts.getSeconds();

	return timestamp
}