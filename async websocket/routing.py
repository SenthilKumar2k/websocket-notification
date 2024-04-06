

# project_name/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from my_app.consumers import NotificationConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/notifications/", NotificationConsumer.as_asgi()),
                ]
            )
        ),
    }
)