$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    var $commendbutton = $("#control").find('button[type="button"]');
    var mouseStillDown = false;

    chatsock.onmessage = function(message) {
        var data = message.data;
        document.getElementById("showmessage").value+=data
    };

    $commendbutton.mousedown(function(event){
        var commend=this.id;
        mouseStillDown=true;
        mouseDownCommend(commend)

        return false;
    });

    $commendbutton.mouseup(function(event){
        mouseStillDown=false;
    });

    function mouseDownCommend(commend)
    { 
        //document.getElementById("showmessage").value+=(commend);
        chatsock.send(commend);
        if (mouseStillDown)
        {
            setTimeout(function(){
                mouseDownCommend(commend)
            }, 100);
        }
    }

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
        if(gamma<0)
        {
            y=Math.abs(gamma);
        }
        else
        {
            y=180-gamma;
        }

        x=90;
        alphamodified = iahtml.innerHTML;

        if (alphamodified<-500)
        {
            setTimeout(function(){
            }, 100); 
            alpha = event.alpha;

            if(gamma<0)
            {
                alpha=alpha+180;
                if (alpha>360)
                {
                    alpha=alpha-360;
                }
            }
<<<<<<< HEAD
            iahtml.innerHTML=Math.round(alpha);
=======
            iahtml.innerHTML=alpha;
>>>>>>> 83d14dada53a6f3c1fd142ba00dd1945cff5e2d7
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

<<<<<<< HEAD
        if (Math.abs(x-formalx)>4 || Math.abs(y-formaly)>4 )
=======
        if (Math.abs(x)>4 || Math.abs(beta-formalbeta)>10 || Math.abs(y-formaly)>4 )
>>>>>>> 83d14dada53a6f3c1fd142ba00dd1945cff5e2d7
        {
            alphadata = Math.round(x);
            gammadata = Math.round(y);

            xhtml.innerHTML = Math.round(x);
            yhtml.innerHTML = Math.round(y);

            var message = {
                x: x,
                y: gammadata,
            }
<<<<<<< HEAD
            chatsock.send(JSON.stringify(message));
            setTimeout(function(){
                mouseDownCommend(commend)
            }, 10);  
=======
            //chatsock.send(JSON.stringify(message));
            setTimeout(function(){
                mouseDownCommend(commend)
            }, 20);  
>>>>>>> 83d14dada53a6f3c1fd142ba00dd1945cff5e2d7
        }

        a.innerHTML = Math.round(alpha);
        b.innerHTML = Math.round(beta);
        g.innerHTML = Math.round(gamma);


    }, false);

});
