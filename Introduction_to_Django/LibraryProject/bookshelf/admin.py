from django.contrib import admin
from .models import Book

# Registering the Book model with the admin interface.
#admin.site.register(Book)  

class BookAdmin(admin.BookAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)