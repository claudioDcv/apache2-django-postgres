from channels.routing import route
from medicalConsultation.consumers import ws_add, ws_disconnect
# from medicalConsultation.consumers import ws_add2, ws_message2, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    # route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    # route("websocket.connect", ws_add2),
    # route("websocket.receive", ws_message2),
    # route("websocket.disconnect", ws_disconnect2),
]
