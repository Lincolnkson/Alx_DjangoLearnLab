from django.db import models

"""Define Complex Models in relationship_app/models.py:

Author Model:
name: CharField.
Book Model:
title: CharField.
author: ForeignKey to Author.
Library Model:
name: CharField.
books: ManyToManyField to Book.
Librarian Model:
name: CharField.
library: OneToOneField to Library."""

class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="libraries")

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, related_name="librarian", on_delete=models.CASCADE)


Librarian = Librarian.objects.prefetch_related("library")
Book = Book.objects.prefetch_related("author")
          
    
    
    


