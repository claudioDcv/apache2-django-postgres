var autimaticScroll = function(){
  var objDiv = document.getElementById("msg-container");
  objDiv.scrollTop = objDiv.scrollHeight;
}


var msgContainer = document.createElement('div');
msgContainer.id = 'msg-container';
document.body.appendChild(msgContainer);

function dump(t){
  console.log(t);
}

var socket = new WebSocket("ws://" + window.location.host + "/updater/");
// socket.onopen = function() {
//   let message = {
//     user : 'front',
//     model: 'None',
//     msg : (new Date()).toString(),
//   }
//   socket.send(JSON.stringify(message));
// }
socket.onmessage = function(e) {
  var msg = JSON.parse(e.data);

  var msgDiv = document.createElement('div');
  msgDiv.className = msg.action;
  var msgDivModel = document.createElement('div');
  var msgDivMsg = document.createElement('div');
  var msgTextModel = document.createTextNode(msg.tag + " : " + msg.object);
  var msgTextMsg = document.createTextNode(msg.action);
  msgDivModel.appendChild(msgTextModel);
  msgDivMsg.appendChild(msgTextMsg);
  msgDiv.appendChild(msgDivModel);
  msgDiv.appendChild(msgDivMsg);
  msgContainer.appendChild(msgDiv);

  autimaticScroll();
  // setTimeout(function () {
  //   var parent = msgDiv.parentElement;
  //   parent.removeChild(msgDiv);
  // }, 3000);
}

if (socket.readyState == WebSocket.OPEN) socket.onopen();



var req = new XMLHttpRequest();
req.open('GET', window.location.origin + '/json-auditor/', true);
req.onreadystatechange = function (aEvt) {
  if (req.readyState == 4) {
     if(req.status == 200){
      // dump(req.responseText);
      var json = JSON.parse(req.responseText);
      // console.log(json);

      for (var i = 0; i < json.total_count; i++) {
        var msg = json.items[i];
        // console.log(elm);
        var msgDiv = document.createElement('div');
        msgDiv.className = msg.action;
        var msgDivModel = document.createElement('div');
        var msgDivMsg = document.createElement('div');
        var msgTextModel = document.createTextNode(msg.tag + " : " + msg.object);
        var msgTextMsg = document.createTextNode(msg.action);
        msgDivModel.appendChild(msgTextModel);
        msgDivMsg.appendChild(msgTextMsg);
        msgDiv.appendChild(msgDivModel);
        msgDiv.appendChild(msgDivMsg);
        msgContainer.appendChild(msgDiv);
      }
      autimaticScroll();
    }else{
      dump("Error loading page\n");
    }
  }
};
req.send(null);
// {% block scripts %}
// <script type="text/javascript">
//
// let chat = document.getElementById('chat');
// let name = document.getElementById('name');
// let msgs = document.getElementById('msgs');
// let txt = document.getElementById('txt');
// let info = document.getElementById('info');
// let loading = document.getElementById('loading')
// let n = 1;
// // Note that the path doesn't matter right now; any WebSocket
// // connection gets bumped over to WebSocket consumers
// socket = new WebSocket("ws://" + window.location.host + "/updater/");
// //socketInfo = new WebSocket("ws://" + window.location.host + "/chat2/");
//
// loading.style.display = 'none'
//
// socket.onmessage = function(e) {
//     //console.log(e.data);
//     let a = document.createElement('div')
//     let b = document.createTextNode(e.data);
//         a.appendChild(b)
//         msgs.appendChild(a)
//
// }
// // socket.onopen = function() {
// //     socket.send("hello world");
// // }
//
// // Call onopen directly if socket is already open
// if (socket.readyState == WebSocket.OPEN) socket.onopen();
//
// socket.onmessage = function(e) {
//     //console.log(e.data);
//
//     let u = document.createElement('strong')
//     let ut = document.createTextNode(JSON.parse(e.data).user);
//         u.appendChild(ut)
//         msgs.appendChild(u)
//
//     let a = document.createElement('p')
//     let b = document.createTextNode(JSON.parse(e.data).msg);
//         a.appendChild(b)
//         msgs.appendChild(a)
//
// }
// // socketInfo.onopen = function() {
// //     //socketInfo.send("hello world");
// // }
//
// // Call onopen directly if socket is already open
// //if (socket.readyState == WebSocket.OPEN) socket.onopen();
//
//
//
// // txt.addEventListener('input',function(e){
// //   loading.style.display = 'block'
// //   socketInfo.send('block');
// // })
// chat.addEventListener('submit',function(e){
//   e.preventDefault();
//   let msg = e.target[1].value;
//   if (n < 2) {
//     name.disabled = true
//   }
//   //n + ": [" + name.value + "] -> " + msg
//   let message = {
//     user : name.value,
//     msg : msg,
//   }
//   socket.send(JSON.stringify(message));
//   e.target[1].value = ''
//   n++;
// })
//
// </script>
// {% endblock %}
