<?php
//Blantly ripped off from https://github.com/donatj/mjpeg-php/blob/master/mjpeg.php
//And then modified to suit out needs

$preview_delay=5000000;


//writeLog("mjpeg stream with $preview_delay delay");

// Used to separate multipart
//$boundary = "PIderman";

// We start with the standard headers. PHP allows us this much
//header ("Content-type: multipart/x-mixed-replace; boundary=$boundary");
//header ("Cache-Control: no-cache");
//header ("Pragma: no-cache");
//header ("Connection: close");

//ob_flush();		//Push out the content we already have (gets the headers to the browser as quickly as possible)

//set_time_limit(0); // Set this so PHP doesn't timeout during a long stream


//ob_start();

//echo "--$boundary\r\n";
//echo "Content-type: image/jpeg\r\n";
     
file_put_contents('mini.png',file_get_contents('convmini.png'));	
//$fileContents = file_get_contents("/var/www/picam/slave/s_cam.jpg");
//$fileContents = file_get_contents("convmini.png");
//$fileLength = strlen($fileContents);

//echo "Content-Length:" . $fileLength . "\r\n";
//echo "\r\n";

//echo $fileContents;

//echo "\r\n";
//ob_end_flush();

usleep($preview_delay);

?>