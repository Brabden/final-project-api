from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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

class KeyboardDetailView(APIView):
    def get(self, request, pk):
        keyboard = get_object_or_404(Keyboard, pk=pk)
        serializer = KeyboardSerializer(keyboard)
        return Response(serializer.data)