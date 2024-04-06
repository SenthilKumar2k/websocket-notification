# my_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "notifications"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

"""
NotificationConsumer (AsyncWebsocketConsumer):

This consumer handles WebSocket connections for receiving and broadcasting notifications in real-time.

During connection (connect() method), it adds the WebSocket connection to the 'notifications' group using 
channel_layer.group_add().

Upon disconnection (disconnect() method), it removes the WebSocket connection from the 'notifications' 
group using channel_layer.group_discard().

When a message is received from a WebSocket client (receive() method), it broadcasts the message to all 
clients in the 'notifications' group using channel_layer.group_send().

The send_notification() method is called when a notification message is received from any client. It 
extracts the message from the event data and sends it back to the client who triggered the event using 
self.send().

Sending Notifications to WebSocket Clients:

When a group message with type "send_notification" is received by any channel in the "notifications" 
group, the send_notification() method is called.It extracts the notification message from the event data 
and sends it to the WebSocket client using self.send().

"""