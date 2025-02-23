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

"""
Task Description:
In your Django project, you will extend the Django User model to include user roles and develop views that restrict access based on these roles. Your task is to set up this system by creating a new model for user profiles, defining views with access restrictions, and configuring URL patterns.

Step 1: Extend the User Model with a UserProfile
Create a UserProfile model that includes a role field with predefined roles. This model should be linked to Django’s built-in User model with a one-to-one relationship.

Fields Required:
user: OneToOneField linked to Django’s User.
role: CharField with choices for ‘Admin’, ‘Librarian’, and ‘Member’.
Automatic Creation: Use Django signals to automatically create a UserProfile when a new user is registered.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class UserProfile:
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('Admin', _('Admin')), ('Librarian', _('Librarian')), ('Member', _('Member'))])

    def __str__(self):
        return self.user.username
    
    


