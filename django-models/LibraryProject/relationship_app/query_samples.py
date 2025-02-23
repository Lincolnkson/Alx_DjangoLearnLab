from relationship_app.models import Author, Book, Library,Librarian
# Define the query for each of the relationship
# Query all books by a specific author.
#["Author.objects.get(name=author_name)", "objects.filter(author=author)"]
#LibraryProject/relationship_app/query_samples.py doesn't contain: ["Author.objects.get(name=author_name)", "objects.filter(author=author)"]
library_name = "Garden City Library"
author_name = "John Doe"

author = Author.objects.get(name=author_name)
author.objects.filter(author=author)
print(author)

# List all books in a library.
books = Library.objects.get(name=library_name)
print(books.books.all())

# # Retrieve the librarian for a library.
# librarian = Library.objects.get(name="library_name").librarian.all()
# print(librarian)

#LibraryProject/relationship_app/query_samples.py doesn't contain: ["Librarian.objects.get(library="]

librarian = Librarian.objects.get(library=library_name)
print(librarian)

# print(Library.objects.get(name="library_name").books.all())
# print("List all books in a library")