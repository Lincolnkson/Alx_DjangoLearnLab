from django.shortcuts import render
from .models import Book,Library
from django.views.generic import ListView


"""
Objective: Develop proficiency in creating both function-based and class-based views in Django, and configuring URL patterns to handle web requests effectively. This task will help you understand different ways to define views and manage URL routing in Django.

Task Description:
In your existing Django project, enhance the relationship_app by adding new views that display information about books and libraries. Implement both function-based and class-based views to handle these displays and configure the URL patterns to route these views correctly.

Steps:
Implement Function-based View:

Create a function-based view in relationship_app/views.py that lists all books stored in the database.
This view should render a simple text list of book titles and their authors."""

# LibraryProject/relationship_app/views.py doesn't contain: ["relationship_app/list_books.html"]
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

"""
Implement Class-based View:

Create a class-based view in relationship_app/views.py that displays details for a specific library, listing all books available in that library.
Utilize Django’s ListView or DetailView to structure this class-based view.
"""

class LibraryBookListView(ListView):
          model = Book
          template_name = 'relationship_app/library__detail.html'
          context_object_name = 'books'
          def get_queryset(self):
                      return Book.objects.filter(library=self.kwargs['pk'])
          

