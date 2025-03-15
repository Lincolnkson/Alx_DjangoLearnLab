
"""
Routing Requirements:
Configure URL patterns in api/urls.py to connect the aforementioned views with specific endpoints.
Each view should have a unique URL path corresponding to its function (e.g., /books/ for the list view, /books/<int:pk>/ for the detail view).
"""
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/update', views.book_update, name='book_update'),
    path('books/delete', views.book_delete, name='book_delete'),
"""
api/urls.py doesn't contain: ["books/update", "books/delete"]

    path('books/<int:pk>/update', views.book_update, name='book_update'),
    path('books/<int:pk>/delete', views.book_delete, name='book_delete'),
"""
]