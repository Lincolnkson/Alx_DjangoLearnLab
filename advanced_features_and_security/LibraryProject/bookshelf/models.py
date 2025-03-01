from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.models import Permission
class Book(models.Model):
          title = models.CharField(max_length=200)
          author = models.CharField(max_length=100)
          publication_year = models.IntegerField()

          permissions =[
               'can_view', 'can_create', 'can_edit','can_delete'
          ]
          
          def __str__(self):
                    return self.title

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


"""
Groups to Setup:
Create groups like Editors, Viewers, and Admins.
Assign appropriate permissions to each group. For example, Editors might have can_edit and can_create permission

"""
class Editors(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)  # Link to the Permission model
    users = models.ManyToManyField(CustomUser)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("can_edit", "Can edit books and publications"),
        ]

class Viewers(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)  # Link to the Permission model
    users = models.ManyToManyField(CustomUser)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("can_view", "Can view books and publications"),
        ]

class Admins(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)  # Link to the Permission model
    users = models.ManyToManyField(CustomUser)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("can_create", "Can create books and publications"),
        ]
    