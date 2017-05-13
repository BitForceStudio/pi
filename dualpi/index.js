var app     = require('express')();
var http    = require('http').Server(app);
//---------------------------------------------
// network

app.get('/', function(req, res){
  res.sendfile(__dirname + '/index.html');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
