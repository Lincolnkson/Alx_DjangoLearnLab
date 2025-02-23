from relationship_app.models import Author, Book, Library,Librarian

# Query all books by a specific author.
library_name = "Garden City Library"
author_name = "John Doe"

author = Author.objects.get(name=author_name)
author.objects.filter(author=author)
print(author)

# List all books in a library.
books = Library.objects.get(name=library_name)
print(books.books.all())

# # Retrieve the librarian for a library.
librarian = Librarian.objects.get(library=library_name)
print(librarian)