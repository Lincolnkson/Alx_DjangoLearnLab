from django.contrib import admin
from .models import Book

# Registering the Book model with the admin interface.
admin.site.register(Book)  
