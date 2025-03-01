from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,BaseUserManager

#Create a custom user manager
"""
create_user: Ensure it handles the new fields correctly.
create_superuser: Ensure administrative users can still be created with the required fields.
"""
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        
        username = self.model.normalize_username(username)
        CustomUser = self.model(username=username, email=email, **extra_fields)
        CustomUser.set_password(password)
        CustomUser.save(using=self._db)

        return CustomUser

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


#Create a custom user model
class CustomUser(AbstractUser):
    """date_of_birth: A date field.
    profile_photo: An image field.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username



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


