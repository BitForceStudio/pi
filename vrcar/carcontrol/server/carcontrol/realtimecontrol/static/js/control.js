$(function() {
    // When we're using HTTPS, use WSS too.
    //var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    //var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    var $commendbutton = $("#control").find('button[type="button"]');
    var mouseStillDown = false;

    //chatsock.onmessage = function(message) {
    //    var data = JSON.parse(message.data);
    //    var msg = $("#showmessage")
        
    //    msg.append(data)
    //};

    $commendbutton.mousedown(function(event){
        var commend=this.id;
        mouseStillDown=true;
        mouseDownCommend(commend)
        //chatsock.send(str(commend));

        //document.getElementById("showmessage").value+="-up";
        return false;
    });

    $commendbutton.mouseup(function(event){
        //var commend=this.id;
        mouseStillDown=false;
        //mouseDownCommend(commend)
        //chatsock.send(str(commend));

        //document.getElementById("showmessage").value+="-up";
        //return false;
    });

    function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    function mouseDownCommend(commend)
    { 
        document.getElementById("showmessage").value+=(commend);

        if (mouseStillDown)
        {
            setTimeout(function(){
                mouseDownCommend(commend)
            }, 100);
        }
    }

});
