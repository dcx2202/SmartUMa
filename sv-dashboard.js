//MAKE AJAX REQUESTS

setInterval(getJSONInfo, 1000), //Cria timer para execucao da funcao a cada segundo


function getJSONInfo()
{
	ajax_get('/apipath', function(data){

		info = data; //data received
		
	});
}

function ajax_get(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {
                //console.log(err.message + " in " + xmlhttp.responseText);
                return;
            }
            callback(data);
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


//HANDLE REQUESTS - SERVER

var express = require('express');
var app = express();

app.use('/lib', express.static('lib'));

app.get('/', function(request, response){

  response.sendFile(__dirname + '/index.html');
})

app.get('/apipath', function(request, response){

  response.jsonp(info_json); //send json
})

app.listen(80);