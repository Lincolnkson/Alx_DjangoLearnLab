from django.urls import path
from .views import book_list,LibraryBookListView, login_view, logout_view

urlpatterns = [
          path('books/',book_list, name='book_list'),
          path('library/<int:pk>/', LibraryBookListView.as_view(), name='library_book_list'),
          path('login/', login_view),
          path('logout/', logout_view, name='logout'),
]

