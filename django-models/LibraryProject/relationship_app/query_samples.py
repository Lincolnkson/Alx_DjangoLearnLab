
from relationship_app.models import Author, Book, Library

"""
Implement Sample Queries:

Prepare a Python script query_samples.py in the relationship_app directory. This script should contain the query for each of the following of relationship:
Query all books by a specific author.
List all books in a library.
Retrieve the librarian for a library.

"""
# Define the query for each of the relationship
# Query all books by a specific author.
author = Author.objects.get(name="John Doe")
books = author.books.all()
print(books)

# List all books in a library.
library = Library.objects.get(name="library_name")
books = library.books.all()
print(books)

# Retrieve the librarian for a library.
librarian = library.librarian.all()
print(librarian)

