from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
from .forms import ExampleForm
# Create your views here.

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