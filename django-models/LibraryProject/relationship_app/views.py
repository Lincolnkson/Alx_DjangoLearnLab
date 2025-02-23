from django.shortcuts import render
from .models import Book
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Library

# LibraryProject/relationship_app/views.py doesn't contain: ["relationship_app/list_books.html"]
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


class LibraryBookListView(ListView):
          model = Book
          template_name = 'relationship_app/library_detail.html'
          context_object_name = 'books'
          def get_queryset(self):
                      return Book.objects.filter(library=self.kwargs['pk'])
          

