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
var DEBUG = true;
var RETRIES = 10;  // max number of retries for I2C calls
//---------------------------------------------


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

init();

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
// motor must be in range 0..1
// value must be in range -128 - +127
// values of -127, -128, +127 are treated as always ON,, no PWM
function setMotor (motor, value)
{
    if (motor>=0 && motor<=1 && value>=-128 && value<128)
    {
        for(var i=0;i<RETRIES;i++)
        {
            try
            {
                wire.writeByteSync(address, motor, value);
                break;
            }
            catch(e)
            {
                if (DEBUG)
                    console.log("Error in set motor, retrying");
            }
        }
    }
}

function forward(speed)
{
    setMotor(0,100);
    setMotor(1,100);
}

function spin(speed)
{
    setMotor(0,-100);
    setMotor(1,100);
}

function stop()
{
    setMotor(0,0);
    setMotor(1,0);
}

//---------------------------------------------

//---------------------------------------------
// network

app.get('/', function(req, res){
  res.sendFile(__dirname + '/move.html');
});

io.on('connection', function(socket){
  socket.on('control', function(msg){
    var data = JSON.parse(msg);
    var x = data.x;
    var y = data.y;
    var xx = Math.min(180, x);
    xx = Math.max(0,  xx);
    var fspeed = 100;//127/90*(xx-90);
    var yy = Math.max(0,  y);
    yy = Math.min(180, yy);
    var sspeed = 0;//127/90*(yy-90);
    if (xx < 10 && xx > -10 && yy < 10 && yy > -10)
    {
      console.log('stop now');
      stop();
    }
    else
    {
      console.log('move');
      forward(fspeed);
      spin(sspeed);
    }
    console.log('message: x  speed: ' + x+'  '+fspeed+' y  speed:'+y+'  '+sspeed);
    sleep.usleep(10);    
  });
});

http.listen(3001, function(){
  console.log('listening on *:3001');
});
