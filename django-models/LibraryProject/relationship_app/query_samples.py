


"""
Implement Sample Queries:

Prepare a Python script query_samples.py in the relationship_app directory. This script should contain the query for each of the following of relationship:
Query all books by a specific author.
List all books in a library.
Retrieve the librarian for a library.

"""
from relationship_app.models import Author, Book, Library

try:
    # Query all books by a specific author
    author = Author.objects.get(name="John Doe")
    books = author.books.all()
    print(f"Author's books: {books}")

    # List all books in a library
    try:
        library = Library.objects.get(name="library_name")
        books = library.books.all()
        print(f"Library books: {books}")

        # Retrieve the librarian(s) for a library
        # Choose the appropriate relationship type:
        try:
            # For one-to-one relationship
            librarian = library.librarian
            print(f"Librarian: {librarian}")
            
            # Or for many-to-many relationship
            # librarian = library.librarian.all()
            # print(f"Librarians: {librarian}")
        except AttributeError:
            print("Check the relationship type between Library and Librarian")
            
    except Library.DoesNotExist:
        print("Library with name 'library_name' not found")
        
except Author.DoesNotExist:
    print("Author 'John Doe' not found")
