# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = 'notifications'
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

"""
This consumer handles WebSocket connections for notifications.

When a WebSocket connection is established, the connect method of the NotificationConsumer is called.

Inside connect, it checks if the user associated with the WebSocket connection is authenticated. 
If authenticated, it adds the connection to the "notifications" group using
async_to_sync(self.channel_layer.group_add).

If the user is not authenticated, the connection is closed using self.close().

When a WebSocket connection is closed, the disconnect method is called. It removes the 
connection from the "notifications" group using async_to_sync(self.channel_layer.group_discard).

Upon connection, it checks if the user is authenticated. If authenticated, it adds the user's 
channel to the 'notifications' group using group_add() and accepts the WebSocket connection. 
The group name is stored in room_group_name.

send_notification method which is called when a notification needs to be sent to the WebSocket client. 
This method sends the notification message to the connected WebSocket client.

This method is called when a message is received from the channel layer with the key "send_notification".
"""

# send notification to both currently connected user and user connected later

"Example snippet 1"

# consumers.py

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = 'notifications'
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Send unsent notifications upon connection
            notifications = Notification.objects.filter(user=self.user)
            for notification in notifications:
                self.send_notification({'message': notification.message})
                notification.delete()

            self.accept()
        else:
            self.close()


"Example snippet 2"

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = 'notifications'
            self.accept()

            # Send stored notifications to the newly connected user
            for notification in self.user.notifications.all():
                self.send_notification({'message': notification.message})
                notification.delete()  # Delete the notification after sending

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))