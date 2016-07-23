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

    window.addEventListener('deviceorientation', function(event) {
        var a = document.getElementById('alpha',
            b = document.getElementById('beta'),
            g = document.getElementById('gamma'),
            alpha = event.alpha,
            beta = event.beta,
            gamma = event.gamma);

      formalalpha=a.innerHTML;
      formalbeta=b.innerHTML;
      formalgamma=g.innerTHML;

      xhtml = document.getElementById('x'),
      yhtml = document.getElementById('y'),

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
      alphamodified = 0;
      if(gamma<0)
      {
          alpha=alpha+180;
          if (alpha>360)
          {
              alpha=alpha-360;
          }
      }
      
      alphamodified = alpha-a.innerHTML;
      x=alphamodified;

      if (Math.abs(alpha-formalalpha)>10 || Math.abs(beta-formalbeta)>10 || Math.abs(y-formaly)>3 )
      {
         alphadata = Math.round(x);
         gammadata = Math.round(y);

         xhtml.innerHTML = Math.round(x);
         yhtml.innerHTML = Math.round(y);

         var message = {
             x: 0,
             y: gammadata,
         }
         chatsock.send(JSON.stringify(message));
         setTimeout(function(){
              mouseDownCommend(commend)
         }, 10);  
      }

      a.innerHTML = Math.round(alpha);
      b.innerHTML = Math.round(beta);
      g.innerHTML = Math.round(gamma);


     }, false);

});
