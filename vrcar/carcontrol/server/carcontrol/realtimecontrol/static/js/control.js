$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);



        var chat = $("#chatroom")
        var $loaduser = $("#loaduser");

        var ele = $('<tr></tr>')
        var clc = $('<td></td>')
        
        var userdata = JSON.parse($loaduser.val());
        var handle = data.handle

        var strinner = ''
        // if message post by me
        if (handle == userdata['ME']['ID'])
        {
            strinner=strinner+'<div class="row" style="margin-left:2px;margin-right:2px"><div class="col-xs-8 col-sm-9 col-lg-10"><div style="float:right;white-space:pre-wrap;word-wrap:break-word;">';
            strinner=strinner+data.message;
            strinner=strinner+'</div></div><div class="col-xs-4 col-sm-3 col-lg-2"><div class="thumbnail" ><img src="http://';
            strinner=strinner+userdata['ME']['THUMB'];
            strinner=strinner+'" alt="';
            strinner=strinner+userdata['ME']['NAME'];
            strinner=strinner+'" class="img-responsive" style="max-height: 35px;"></div></div></div>';
        }
        // message come from other
        else
        {
            strinner=strinner+'<div class="row" style="margin-left:2px;margin-right:2px"><div class="col-xs-4 col-sm-3 col-lg-2"><div class="thumbnail" ><img src="http://';
            strinner=strinner+userdata['YO']['THUMB'];
            strinner=strinner+'" alt="';
            strinner=strinner+userdata['YO']['NAME'];
            strinner=strinner+'" class="img-responsive" style="max-height: 35px;"></div></div><div class="col-xs-8 col-sm-9 col-lg-10"><div  style="float:left;white-space:pre-wrap;word-wrap:break-word;">';
            strinner=strinner+data.message;
            strinner=strinner+'</div></div></div>';
        }

        clc.append(strinner)
        ele.append(clc)
        
        chat.append(ele)
        updateScroll();
    };

    $("#control").on("submit", function(event) {
        var commend=this.id
        chatsock.send(str(commend));

        return false;
    });
});
