from django.shortcuts import render

# Create your views here.
"""
Define the View:
In api/views.py, create a view named BookList that extends rest_framework.generics.ListAPIView.
Use the BookSerializer to serialize the data and the Book model as the queryset.
"""
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#Use rest_framework.permissions to apply basic permissions like IsAuthenticated, IsAdminUser
class BookViewSet(viewsets.ModelViewSet):
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated,IsAdminUser]
     
     queryset = Book.objects.all()
     serializer_class = BookSerializer

"""
Step 2: Generate and Use Tokens
Provide a way for users to obtain a token and use it for authenticated requests.

Token Retrieval Endpoint:
Implement a view that allows users to obtain a token by providing their username and password.
This can be done using DRF’s built-in views like obtain_auth_token.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
