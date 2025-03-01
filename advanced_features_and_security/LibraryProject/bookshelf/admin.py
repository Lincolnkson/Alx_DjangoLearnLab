from django.contrib import admin
from .models import Book,CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(UserAdmin):
    # Add the new fields to the admin display
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Include new fields in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Add new fields to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Allow filtering by date of birth
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Add date_of_birth to search fields
    search_fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')

# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
# This line registers the Book model with the admin interface.
#admin.site.register(Book)  

class BookAdmin(admin.ModelAdmin):
          list_display = ('title', 'author', 'publication_year')
          list_filter = ('author', 'publication_year')
          search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)



