# from django.http import HttpResponse
# from channels.handler import AsgiHandler
# In consumers.py
from channels import Group


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("updater").add(message.reply_channel)


# Connected to websocket.receive
# def ws_message(message):
#   message = json.loads(message.content['text'])
#   Group("chat").send({
#     "text": message.content['text']  # "[user] %s" % message.content['text'
#   })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("updater").discard(message.reply_channel)


# Connected to websocket.connect
# def ws_add2(message):
#     # Accept the connection
#     message.reply_channel.send({"accept": True})
#     # Add to the chat group
#     Group("chat2").add(message.reply_channel)
#
#
# # Connected to websocket.receive
# def ws_message2(message):
#     Group("chat2").send({
#         "text": "[user] %s" % message.content['text'],
#     })
#
#
# # Connected to websocket.disconnect
# def ws_disconnect2(message):
#     Group("chat2").discard(message.reply_channel)

# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse(
#         "Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)
#
#
# def ws_message(message):
#     # ASGI WebSocket packet-received and send-packet message types
#     # both have a "text" key for their textual data.
#     message.reply_channel.send({
#         "text": message.content['text'],
#     })
