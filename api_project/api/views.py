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

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer