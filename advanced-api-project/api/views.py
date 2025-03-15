from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

#Creating generic CRUD functionality
class BookListView(generics.ListAPIView):
    """
     API endpoint that allows books to be listed.
    Authentication:
    - Requires user authentication via token or session
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BookSerializer
    def get_queryset(self):
        queryset = Book.objects.all()
        
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
    
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows a specific book to be viewed.
    
    This view returns the details of a single book identified by its primary key.
    Results are filtered by authentication and optional username filtering.
    
    Authentication:
    - Requires user authentication via token or session

    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BookSerializer
    def get_queryset(self):
        queryset = Book.objects.all()
        
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
    
        return queryset

class BookCreateView(generics.CreateAPIView):
    """
    API endpoint that allows new books to be created.
    
    Authentication:
    - Requires user authentication via token or session
    """
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows existing books to be updated.
    
    Supports both PUT (complete update) and PATCH (partial update) methods.
    
    Authentication:
    - Requires user authentication via token or session
    """
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint that allows books to be deleted.
    
    Authentication:
    - Requires user authentication via token or session
    """
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
