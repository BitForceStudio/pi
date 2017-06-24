var express = require('express');
var app     = require('express')();
var http    = require('http').Server(app);

//---------------------------------------------
// network

app.use( express.static(__dirname));

app.get('/', function(req, res){
  res.sendfile(__dirname + '/index.html');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
