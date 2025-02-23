"""
Configure URL Patterns:

Edit relationship_app/urls.py to include URL patterns that route to the newly created views. Make sure to link both the function-based and class-based views.
"""
from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
          path('books/',list_books, name='book_list'),
          path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_book_list'),
]

