function setDuration (numMinutes){
	var ts = new Date();
	minutes = (ts.getMinutes()-numMinutes) >0 ? (ts.getMinutes()-numMinutes) : 0
	timestamp = ts.getFullYear()+"-"+(ts.getMonth()+1)+"-"+ts.getDate()+" "+ts.getHours()+":"+ minutes	+":"+ts.getSeconds();

	return timestamp
}