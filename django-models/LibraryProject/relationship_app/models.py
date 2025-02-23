from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    # Add __str__ method to Author model
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name
class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, related_name="librarian", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

Librarian = Librarian.objects.prefetch_related("library")
Book = Book.objects.prefetch_related("author")
          
    
    
    


