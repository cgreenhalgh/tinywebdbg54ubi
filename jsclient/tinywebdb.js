// TinyWebDB example Javascript Client.
// Requires JQuery and JQuery.JSON
// Chris Greenhalgh (cmg@cs.nott.ac.uk), The University of Nottingham, 2011-03-16

//$.ajaxSetup({cache:false,async:false,timeout:30000});

//alert('tinywebdb.js');

function log1(msg) {
	try {
		log(msg);
	}
	catch (err) {
		alert(msg);
		// no-op
	}
}

function do_post(url, data, callback) {
	try {
//		log1('POST '+data+' to '+url);
		var req = $.ajax({url: url, 
			cache: false,
			async: (callback!=undefined),
			timeout: 30000,
			type: 'POST',
			//default: contentType: 'application/x-www-form-urlencoded',
			//processData: true,
			data: data,
			dataType: 'json',
			success: function success(data, status) {
//				log1('TinyWebDB success: '+data);
				if (callback!=undefined) {
					if (data!=undefined && data[2]!=undefined)
						callback(data[2]);
					else
						log1('TinyWebDB bad response: '+data);
				}
			},
			error: function error(req, status, err) {
				log1('TinyWebDB error: '+status+' ('+(err!=undefined ? err.message : '')+(err!=undefined ? ': '+err.description : '')+')');
//				log1('readyState='+req.readyState+', status='+req.status+', statusText='+req.statusText+', responseText='+req.responseText);
			}
		});
		var response = req.responseText;
		if (response!=undefined) {
			var json = $.parseJSON(response);
//			log1('Get JSON response '+json);
			if (json!=undefined && json[2]!=undefined)
				return json[2];
			else
				log1('TinyWebDB bad response (sync): '+response);				
		}
		return response;
//		log1('readyState='+req.readyState+', status='+req.status+', statusText='+req.statusText+', responseText='+req.responseText);
	} catch (err) {
		log1('TinyWebDB exception: '+err.message);
		return undefined;
	}
}

function get_value(url, tag, callback) {
    var data = {tag: tag};
	url = url+'getvalue';
    return do_post(url, data, callback);
}

function set_value(url, tag, value, callback) {
    var data = {tag: tag, value: value};
	url = url+'storeavalue';
    return do_post(url, data, callback);
}
