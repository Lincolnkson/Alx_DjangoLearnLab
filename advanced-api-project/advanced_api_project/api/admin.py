from django.contrib import admin
from .models import Book, Author


class BookAdmin(admin.ModelAdmin):
          list_display = ('title', 'publication_year', 'author')

class AuthorAdmin(admin.ModelAdmin):
          list_display = ('name',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)


