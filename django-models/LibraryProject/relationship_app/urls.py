from django.urls import path
from .views import list_books,LibraryDetailView, login_view, logout_view, register #, admin, librarian, member
 #["from .views import list_books", "LibraryDetailView"]
"""
["views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="]
"""
urlpatterns = [
          path('books/',list_books, name='list_books'),
          path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_book_list'),
          path('login/', login_view),
          path('logout/', logout_view, name='logout'),
          path('register/', register.as_view(), name='register'),

          # path('admin/', admin.as_view(), name='admin'),
          # path('librarian/', librarian, name='librarian'),
          # path('member/', member.as_view(), name='member'),
          # path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_book_list'),
]


"""
Step 3: Configure URL Patterns
Define URL patterns that will route to the newly created role-specific views. Ensure that each URL is correctly linked to its respective view and that the URLs are named for easy reference.

URLs to Define:
A URL for the ‘Admin’ view.
A URL for the ‘Librarian’ view.
A URL for the ‘Member’ view.
"""