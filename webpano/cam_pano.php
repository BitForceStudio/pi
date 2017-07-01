<?php
  header("Content-Type: image/jpeg");
   $preview_delay = 100000;
   usleep($preview_delay);
   readfile("img/viewpano.png");
?>