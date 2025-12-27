from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Keyboard
from .serializers import KeyboardSerializer

class KeyboardListCreateView(APIView):
    def get(self, request):
        keyboards = Keyboard.objects.all()
        serializer = KeyboardSerializer(keyboards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = KeyboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

