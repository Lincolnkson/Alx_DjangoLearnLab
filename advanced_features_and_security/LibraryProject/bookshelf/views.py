from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
from .forms import ExampleForm
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
    
    query = request.GET.get('q', '')
    # SAFE: ORM filters automatically sanitize inputs
    results = books.objects.filter(title__icontains=query)
    
    return render(request, 'bookshelf/book_list.html', {'books': results})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return HttpResponse("Book created successfully")
    return render(request, 'bookshelf/form_example.html',ExampleForm)


#Create view that contains: ["from .forms import ExampleForm"]
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponse("Book updated successfully")
    else:
        form = ExampleForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form})