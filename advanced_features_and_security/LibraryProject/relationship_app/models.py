from django.db import models
from django.contrib.auth.models import User
from bookshelf.models import CustomUser

class Author(models.Model):
    name = models.CharField(max_length=255)

    # Add __str__ method to Author model
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    class Meta:
        permissions =[
            "can_add_book",
            "can_change_book",
            "can_delete_book"
        ]
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

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class UserProfile(models.Model):
    #Define the choices for the role field
    Admin = 'Admin'
    Librarian = 'Librarian'
    Member = 'Member'
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    ]
    
    CustomUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    
    def __str__(self):
        return f"{self.CustomUser.username} - {self.role}"

# Signal to create UserProfile when a new User is created
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(CustomUser=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


