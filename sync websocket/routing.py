# routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.consumers import NotificationConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/notifications/$', NotificationConsumer),
        ])
    ),
})

"""This file configures routing for WebSocket connections. It maps WebSocket paths to consumers.

The ProtocolTypeRouter is used to route WebSocket connections to the appropriate consumer.

It imports NotificationConsumer from myapp.consumers and sets it to handle WebSocket connections 
on the path ws/notifications/.

The AuthMiddlewareStack ensures that WebSocket connections are handled only for authenticated users.
"""



#or
#from myapp.routing import websocket_urlpatterns
# websocket_urlpatterns = [
#     path('ws/notifications/', NotificationConsumer),
# ]

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })