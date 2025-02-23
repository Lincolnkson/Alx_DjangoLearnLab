"""
Configure URL Patterns:

Edit relationship_app/urls.py to include URL patterns that route to the newly created views. Make sure to link both the function-based and class-based views.
"""
from django.urls import path
from . import views

urlpatterns = [
          path('books/', views.book_list, name='book_list'),
          path('library/<int:pk>/', views.LibraryBookListView.as_view(), name='library_book_list'),
]

