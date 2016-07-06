$(function() {
    // When we're using HTTPS, use WSS too.
    //var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    //var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    var $commendbutton = $("#control").find('button[type="button"]');
    
    //chatsock.onmessage = function(message) {
    //    var data = JSON.parse(message.data);
    //    var msg = $("#showmessage")
        
    //    msg.append(data)
    //};

    $commendbutton.on("click",function(event){
        var commend=this.id;
        //chatsock.send(str(commend));

        //document.getElementById("showmessage").value+="-up";
        return false;
    });

    //document.body.onmousedown = function() { 
    //    document.getElementById("showmessage").value+="+up";
    //}

});
