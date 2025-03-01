from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
# Create your views here.
"""
Modify your views to check for these permissions before allowing users to perform certain actions. Use decorators such as permission_required to enforce these permissions in your views.

Views to Modify or Create:
Ensure views that create, edit, or delete model instances check for the correct permissions.
Example: Use @permission_required('app_name.can_edit', raise_exception=True) to protect an edit view.

LibraryProject/bookshelf/views.py doesn't contain: ["book_list", "raise_exception", "books"]
"""

@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return HttpResponse("Book created successfully")
    return render(request, 'create_book.html')
