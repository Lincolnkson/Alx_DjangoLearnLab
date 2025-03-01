# from django.contrib import admin
# from .models import Book

# # Registering the Book model with the admin interface.
# #admin.site.register(Book)  

# # - LibraryProject/bookshelf/admin.py doesn't contain: ["admin.ModelAdmin"]
# #LibraryProject/bookshelf/admin.py contains: ["admin.BookAdmin"]

# class BookAdmin(admin.BookAdmin):
#     list_display = ('title', 'author', 'published_date')
#     search_fields = ('title', 'author')

# admin.site.register(Book, BookAdmin)


# """
# Task Description:
# Enhance your bookshelf app by integrating the Book model with the Django admin interface. Customize the admin display to improve the management and visibility of book data, and document the process to ensure consistent setup and configuration.

# Steps:
# 1. Register the Book Model with the Django Admin:
# """

from django.contrib import admin
from .models import Book

# This line registers the Book model with the admin interface.
#admin.site.register(Book)  

class BookAdmin(admin.ModelAdmin):
          list_display = ('title', 'author', 'publication_year')
          list_filter = ('author', 'publication_year')
          search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)



