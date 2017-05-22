var express = require('express');
var app     = require('express')();
var http    = require('http').Server(app);
var io      = require('socket.io')(http);
var sleep   = require('sleep');

// I2C driver
var i2c = require('i2c-bus'),
   wire = i2c.openSync(1);
var address = 0x22;

var MOTORA    = 0;
var OUTCFG0   = 2;
var OUTPUT0   = 8;
var INCFG0    = 14;
var SETBRIGHT = 18;
var UPDATENOW = 19;
var RESET     = 20;

//---------------------------------------------
// General variables
var DEBUG = false;
var RETRIES = 10;  // max number of retries for I2C calls
//---------------------------------------------

var pan  = 0;
var tilt = 1;
var step = 5;

try{
  initall();
}
catch(e){
  console.log("define 2 i2c error"+e);
}

var panVal = 90;
var tiltVal = 90;

function initall(){
  // init
  init(true);
  setOutputConfig(pan, 2);
  setOutputConfig(tilt, 2);
  setOutput(pan,  90 );
  setOutput(tilt, 90 );
}

//---------------------------------------------
// Initialise the Board (same as cleanup)
function init(debug=false){
  DEBUG = debug;
  for (var i=0;i<RETRIES;i++){
    try{
      wire.writeByteSync(address, RESET, 0);
      break;
    }
    catch(e){
      if (DEBUG)
        console.log("Error in init(), retrying");
    }
  }
  sleep.usleep(10);  //1ms delay to allow time to complete
  if (DEBUG)
    console.log("Debug is", DEBUG);
}
//---------------------------------------------

//---------------------------------------------
// Cleanup the Board (same as init)
function cleanup()
{
  for (var i=0;i<RETRIES;i++){
    try{
      wire.writeByteSync(address, RESET, 0);
      break;
    }
    catch(e){
      if (DEBUG)
        console.log("Error in cleanup(), retrying");
    }
  }
  console.log('clean up')
  sleep.usleep(1)   // 1ms delay to allow time to complete
}
//---------------------------------------------

//---------------------------------------------
// Set configuration of selected output
// 0: On/Off, 1: PWM, 2: Servo, 3: WS2812B
function setOutputConfig (output, value){
  if (output>=0 && output<=5 && value>=0 && value<=3){
    if (DEBUG)
      console.log("set output config called, cmd:"+output+" value:"+value);
    for (var i=0;i<RETRIES;i++){
      try{
        wire.writeByteSync(address, OUTCFG0+output, value);
        break;
      }
      catch(e){
        if (DEBUG)
          console.log("Error in setOutputConfig(), retrying");
      }
    }
  }
}
//---------------------------------------------

//---------------------------------------------
// Set output data for selected output channel
// Mode  Name    Type    Values
// 0     On/Off  Byte    0 is OFF, 1 is ON
// 1     PWM     Byte    0 to 100 percentage of ON time
// 2     Servo   Byte    -100 to + 100 Position in degrees
// 3     WS2812B 4 Bytes 0:Pixel ID, 1:Red, 2:Green, 3:Blue
function setOutput (channel, value){
  if (channel>=0 && channel<=5){
    if (DEBUG)
      console.log("set output called");
    for (var i=0;i<RETRIES;i++){
      try{
        wire.writeByteSync(address, OUTPUT0 + channel, value);
        if(DEBUG)
          console.log('set output, channel: '+channel+" value:"+value);
        break;
      }
      catch(e){
        if (DEBUG)
          console.log("Error in setOutput(), retrying"+e+" "+value);
      }
    }
    if (i==RETRIES){
      cleanup();
    }
  }
}
//---------------------------------------------
// network

app.use( express.static(__dirname));

app.get('/', function(req, res){
  res.sendfile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  socket.on('control', function(msg){
    var data = JSON.parse(msg);
    var x = data.x;
    var y = 180-data.y;
    console.log('message: x: ' + x+' y:'+y);
    var xx = Math.min(140, x);
    xx = Math.max(40,  xx);
    setOutput (tilt, xx);
    var yy = Math.max(40,  y);
    yy = Math.min(150, yy);
    setOutput (pan, yy);
    sleep.usleep(10);    
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
