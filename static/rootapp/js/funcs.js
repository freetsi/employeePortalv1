// JQuery functions

// Ajax request for log

function exportLog(elm, elmDate, elmTarget, elmSize, dir) {
    logname = $(elm).val();
    logdate = $(elmDate).val();
    var url_first_half = "/api/v1/logs/log/?log=".concat(logname);
    var url_second_half = url_first_half.concat("&idx=-1&size=200&download=true&logdate=");
    var url_full = url_second_half.concat(logdate);
    window.location.href = url_full
}

function getLogSelected(elm, elmDate, elmTarget, elmSize, dir) {
	logname = $(elm).val();
	logdate = $(elmDate).val();
	url = '/api/v1/logs/log/';

	size = $(elmSize).val() - 0;
	start = $(elmTarget).attr("logstart") - 0;
	start = (dir=='up') ? Math.max(start-size, 0) : (dir!='same') ? start+size : -2;
	jqueryA.getJSON(url, { "log": logname, "idx": start, 'size': size, 'logdate': logdate
	}).done(function(logdata){
//		console.log(logdata);
		$(elmTarget).attr("logstart", logdata['start']);
		$(elmTarget).attr("logstop", logdata['stop']);
		$(elmTarget).text(logdata['log']);

		$("#goUp").prop("disabled", !(logdata['start'] > 0))
		$("#goDown").prop("disabled", (logdata['stop'] - logdata['start'] < size))

	}).fail(function(text){
		console.log(text);
		window.location.href = "/";
	});
}
