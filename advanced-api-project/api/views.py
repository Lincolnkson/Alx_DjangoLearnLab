from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
# from django_filters import rest_framework

#Creating generic CRUD functionality
class BookListView(generics.ListAPIView):
    """
     API endpoint that allows books to be listed.
    Authentication:
    - Requires user authentication via token or session

        Filtering:
    - Supports filtering by title, author, publication_year, and purchaser username
    - All filters are applied via query parameters
    
    Searching:
    - Supports full-text search across title and author fields
    - Search is case-insensitive
    
    Ordering:
    - Supports ordering by title and publication_year fields
    
    Example Requests:
    1. Filter by title:         GET /api/books/?title=django
    2. Filter by author:        GET /api/books/?author=martin
    3. Filter by year:          GET /api/books/?publication_year=2023
    4. Filter by username:      GET /api/books/?username=johndoe
    5. Search all fields:       GET /api/books/?search=python
    6. Order by title:          GET /api/books/?ordering=title
    7. Order by year descending: GET /api/books/?ordering=-publication_year
    8. Combined filters:        GET /api/books/?title=django&username=johndoe
    
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BookSerializer
    def get_queryset(self):
        queryset = Book.objects.all()


        #Integrate Django REST Framework’s filtering capabilities to allow users to filter the book list by various attributes like title, author, and publication_year.
        query_params = self.request.query_params
        title = query_params.get('title')
        author = query_params.get('author')
        publication_year = query_params.get('publication_year')

        # Apply filters if parameters are provided
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:  # Changed from 'elif' to 'if' to allow multiple filters
            queryset = queryset.filter(author__icontains=author)
        if publication_year:  # Changed from 'elif' to 'if' to allow multiple filters
            queryset = queryset.filter(publication_year=publication_year)
        
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
    
        return queryset
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'publication_year']

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
