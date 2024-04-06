from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageView(APIView):
    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
