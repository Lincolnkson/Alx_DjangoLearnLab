# Alx_DjangoLearnLab

Tasks
0. Introduction to Django Development Environment Setup
1. Implementing and Interacting with Django Models
2. Utilizing the Django Admin Interface

Week 10 
0. Implementing Advanced Model Relationships in Django
1. Django Views and URL Configuration


# Django User Permissions and Groups Setup Guide

This document outlines how the custom user model, permissions, and user groups are set up and used in the Library Project application.

## Custom User Model

The application uses a custom user model `CustomUser` that extends Django's `AbstractUser` with additional fields:

- `date_of_birth`: A date field for storing the user's birth date
- `profile_photo`: An image field for storing the user's profile picture

## Permission System

### Available Permissions

The application defines the following custom permissions:

- `can_view`: Allows users to view books and publications
- `can_edit`: Allows users to modify existing books and publications
- `can_create`: Allows users to add new books and publications
- `can_delete`: Allows users to remove books from the system

### User Groups

The application organizes users into three primary groups, each with specific permissions:

1. **Viewers**
   - Has the `can_view` permission
   - Can browse and read book information
   - Cannot make any changes to the data

2. **Editors**
   - Has the `can_edit` permission
   - Can modify existing book information
   - Cannot add new books or delete existing ones

3. **Admins**
   - Has the `can_create` permission
   - Also implicitly has all other permissions
   - Can manage all aspects of books and publications

## Implementation Details

### Models

- Permissions are defined in the `Meta` class of their respective models
- The Book model includes all available permissions
- Each group model (`Editors`, `Viewers`, `Admins`) has its specific permissions

### Usage in Views

To restrict access to views based on permissions:

```python
from django.contrib.auth.decorators import user_passes_test

# For admin-only views
def has_admin_permissions(user):
    return user.has_perms(['bookshelf.can_create'])

@user_passes_test(has_admin_permissions)
def admin_view(request):
    # Admin functionality here
    pass

# For editor views
def has_editor_permissions(user):
    return user.has_perms(['bookshelf.can_edit'])

@user_passes_test(has_editor_permissions)
def update_book(request, pk):
    # Book updating functionality here
    pass

# For views accessible to viewers
def has_viewer_permissions(user):
    return user.has_perms(['bookshelf.can_view'])

@user_passes_test(has_viewer_permissions)
def list_books(request):
    # Book listing functionality here
    pass
```

## Adding Users to Groups

You can add users to groups either programmatically or through the admin interface:

### Via Admin Interface

1. Access the Django admin panel
2. Navigate to the Users section
3. Select a user
4. Assign them to the appropriate group(s)

### Programmatically

```python
from django.apps import apps

# Get the group models
Editors = apps.get_model('bookshelf', 'Editors')
Viewers = apps.get_model('bookshelf', 'Viewers')
Admins = apps.get_model('bookshelf', 'Admins')

# Create a new editor group
editor_group = Editors.objects.create(name='Content Editors')

# Add a user to the editor group
user = CustomUser.objects.get(username='editor_user')
editor_group.users.add(user)
```

## Best Practices

1. Always check permissions before performing restricted actions
2. Use the `@permission_required` or `@user_passes_test` decorators for view protection
3. For class-based views, use `PermissionRequiredMixin`
4. Assign users to the most restrictive group that meets their needs