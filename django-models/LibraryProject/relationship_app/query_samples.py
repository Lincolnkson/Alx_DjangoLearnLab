from relationship_app.models import Author, Book, Library
# Define the query for each of the relationship
# Query all books by a specific author.
# author = Author.objects.get(name="John Doe")
# books = author.books.all()
# print(books)

# # List all books in a library.
# books = Library.objects.get(name="library_name").books.all()
# print(books)

# # Retrieve the librarian for a library.
# librarian = Library.objects.get(name="library_name").librarian.all()
# print(librarian)

print(Library.objects.get(name="library_name").books.all())
print("List all books in a library")