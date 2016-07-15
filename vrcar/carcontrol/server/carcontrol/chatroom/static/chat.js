$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});


if(window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', function(event) {
  var a = document.getElementById('alpha',
          b = document.getElementById('beta'),
          g = document.getElementById('gamma'),
          alpha = event.alpha,
          beta = event.beta,
              gamma = event.gamma;

  a.innerHTML = Math.round(alpha);
  b.innerHTML = Math.round(beta);
  g.innerHTML = Math.round(gamma);

    }, false);
}else{
    document.querySelector('body').innerHTML = '你的瀏覽器不支援喔';
}