//
// MJPEG
//
var $mjpeg_left_img=$("#mjpeg_left");
var ip_left ="http://192.168.1.8:80"

var halted = 0;
var previous_halted = 99;
var mjpeg_mode = 0;
var preview_delay = 0;
var socket = io();
var sampletime = 10;

$(function() {

    //reload_img();
    //updatePreview(true);

    window.addEventListener('deviceorientation', function(event) 
    {
        var a = document.getElementById('alpha');
        var b = document.getElementById('beta');
        var g = document.getElementById('gamma');
        var alpha = event.alpha;
        var beta  = event.beta;
        var gamma = event.gamma;

        formalalpha=a.innerHTML;
        formalbeta=b.innerHTML;
        formalgamma=g.innerTHML;

        xhtml = document.getElementById('x'),
        yhtml = document.getElementById('y'),
        iahtml = document.getElementById('curralpha'),

        formaly=yhtml.innerHTML;
        formalx=xhtml.innerHTML;

        y=90;
        if(gamma<0) { y=Math.abs(gamma); }
        else        { y=180-gamma;       }

        x=90;
        alphamodified = iahtml.innerHTML;

        if (alphamodified<-500)
        {
            setTimeout(function(){}, 100); 
            alpha = event.alpha;

            if(gamma<0)
            {
                alpha=alpha+180;
                if (alpha>360)
                {
                    alpha=alpha-360;
                }
            }
            iahtml.innerHTML=Math.round(alpha);
        }

        if(gamma<0)
        {
            alpha=alpha+180;
            if (alpha>360)
            {
                alpha=alpha-360;
            }
        }

        alphacurrent = iahtml.innerHTML;
        alphachange=Math.round(alpha)-alphacurrent;
      
        x = alphachange+90;

        if (Math.abs(x-formalx)>4 || Math.abs(y-formaly)>4 )
        {
            alphadata = Math.round(x);
            gammadata = Math.round(y);

            xhtml.innerHTML = Math.round(x);
            yhtml.innerHTML = Math.round(y);

            var message = {
                x: x,
                y: gammadata,
            }
            socket.emit('control', JSON.stringify(message));

            setTimeout(function(){}, sampletime);  
        }

        a.innerHTML = Math.round(alpha);
        b.innerHTML = Math.round(beta);
        g.innerHTML = Math.round(gamma);


    }, false);

});

function toggle_fullscreen(e) {

    var background = document.getElementById("background");

    if(!background) {
        background = document.createElement("div");
        background.id = "background";
        document.body.appendChild(background);
    }
  
    if(e.className == "fullscreen") {
        e.className = "";
        background.style.display = "none";
    }
    else {
        e.className = "fullscreen";
        background.style.display = "block";
    }

}

function reload_img () {
    if(!halted) 
    {
        $mjpeg_left_img[0].src = ip_left+"/cam_pic.php?time=" + new Date().getTime() + "&pDelay=" + preview_delay;
    }
    else 
    {
        setTimeout("reload_img()", 500);
    }
}

function error_img () {
    setTimeout("mjpeg_left_img.src = "+ip_left+"'/cam_pic.php?time=' + new Date().getTime();", 100);
}

function updatePreview(cycle)
{
    if (cycle !== undefined && cycle == true)
    {
        $mjpeg_left_img[0].src = ip_left+"/updating.jpg";
        setTimeout("$mjpeg_left_img[0].src = \" " + ip_left + "/cam_pic_new.php?time=\" + new Date().getTime()  + \"&pDelay=\" + preview_delay;", 1000);
        return;
    }
  
    if (previous_halted != halted)
    {
        if(!halted)
        {
            $mjpeg_left_img[0].src = ip_left+"/cam_pic.php?time=" + new Date().getTime() + "&pDelay=" + preview_delay;
        }
        else
        {
            $mjpeg_left_img[0].src = ip_left+"/updating.jpg";
        }
    }
    previous_halted = halted;

}

