# views.py
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if message:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": message,
                }
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'No message provided'}, status=400)
        
"""
This view handles POST requests to create new notifications.

gets the channel layer using get_channel_layer(). The channel layer is a communication 
backend that allows different parts of your application to communicate with each other.

Next, it uses async_to_sync to wrap the call to channel_layer.group_send(). This function 
sends a message to a group of channels (in this case, the "notifications" group).

The message sent to the group contains a type (send_notification) and the message itself.

Finally, it returns a JSON response indicating success if a message was provided, or 
failure with an error message if no message was provided.

When a POST request is received with a message, it sends a notification message to 
the "notifications" group using the channel layer.

"""



# Update NotificationView to send notifications to all registered users instead 
# of sending them to a WebSocket group.

class NotificationView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if message:
            users = User.objects.all()
            channel_layer = get_channel_layer()
            for user in users:
                async_to_sync(channel_layer.send)(
                    f"user_{user.id}",
                    {
                        "type": "send_notification",
                        "message": message,
                    }
                )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'No message provided'}, status=400)
        


# send notification to both currently connected user and user connected later

"Example snippet 1"

from myapp.models import Notification  # Assuming you have a Notification model

class NotificationView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if message:
            # Save the notification in the database for all users
            users = User.objects.all()
            for user in users:
                Notification.objects.create(user=user, message=message)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'No message provided'}, status=400)
        

"Example snippet 2"

class NotificationView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if message:
            # Store the notification temporarily
            Notification.objects.create(user=request.user, message=message)
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": message,
                }
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'No message provided'}, status=400)