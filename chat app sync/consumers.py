# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        username = self.scope['user'].username  # Assuming you're using Django's built-in authentication

        # Save message to database
        ChatMessage.objects.create(user=self.scope['user'], message=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))



"""To convert the ChatConsumer from WebsocketConsumer to AsyncWebsocketConsumer in Django Channels, 
you need to use asynchronous features provided by Python's asyncio library."""

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username  # Assuming you're using Django's built-in authentication

        # Save message to database asynchronously (assuming you've already defined the ChatMessage model)
        await ChatMessage.objects.create(user=self.scope['user'], message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


#Changes made:

1) Import AsyncWebsocketConsumer instead of WebsocketConsumer.
2) Methods are defined with async def to make them asynchronous.
3) await is used for asynchronous calls to methods like group_add, group_discard, and group_send.
4) Message saving to the database (assuming you have a ChatMessage model) is done asynchronously using await.
5) Sending messages to the WebSocket is done asynchronously using await self.send().