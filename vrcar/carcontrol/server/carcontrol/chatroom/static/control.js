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

});
