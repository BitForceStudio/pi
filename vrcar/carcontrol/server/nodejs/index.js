var app     = require('express')();
var http    = require('http').Server(app);
var io      = require('socket.io')(http);
var sleep   = require('sleep');


// I2C driver
var i2c     = require('i2c');
var address = 0x22;

var MOTORA    = 0
var OUTCFG0   = 2
var OUTPUT0   = 8
var INCFG0    = 14
var SETBRIGHT = 18
var UPDATENOW = 19
var RESET     = 20

//---------------------------------------------
// General variables
var DEBUG = False
var RETRIES = 10  // max number of retries for I2C calls
//---------------------------------------------

var pan = 0
var tilt = 1
var step = 5


var wire = new i2c(address, {device: '/dev/i2c-1'});

setOutputConfig()

//---------------------------------------------
// Initialise the Board (same as cleanup)
function init (debug=False){
  DEBUG = debug；
  for (var i=0;i<RETRIES;i++){
    try{
      wire.writeBytes(RESET, 0)；
      break；
    }
    except{
      if (DEBUG)
        console.log("Error in init(), retrying")；
    }
  }
  sleep.usleep(10)  //1ms delay to allow time to complete
  if (DEBUG)
    console.log("Debug is", DEBUG);
}
//---------------------------------------------

//---------------------------------------------
// Cleanup the Board (same as init)
function cleanup ()
{
  for (var i=0;i<RETRIES;i++){
    try{
      wire.writeBytes(RESET, 0);
      break;
    }
    except(e){
      if (DEBUG)
        console.log("Error in cleanup(), retrying");
    }
  }
  sleep.usleep(1)   # 1ms delay to allow time to complete
}
//---------------------------------------------

//---------------------------------------------
// Set configuration of selected output
// 0: On/Off, 1: PWM, 2: Servo, 3: WS2812B
function setOutputConfig (output, value){
  if (output>=0 && output<=5 && value>=0 && value<=3){
    for (var i=0;i<RETRIES;i++){
      try{
        wire.writeBytes(OUTCFG0 + output, value, function(err){
          if (err)
        	  console.log('writeBytes error'+err)
        });
        break;
      }
      except(e){
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
    for (var i=0;i<RETRIES;i++){
      try{
        wire.writeBytes(OUTPUT0 + channel, value, function(err){
          if (err)
            console.log('writeBytes error'+err)
        });
        break;
      }
      except(e){
        if (DEBUG)
          console.log("Error in setOutput(), retrying");
      }
    }
}
//---------------------------------------------
// network

app.get('/', function(req, res){
  res.sendfile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  socket.on('control', function(msg){
    console.log('message: ' + msg);

    

  });
  // need to call the python script
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});