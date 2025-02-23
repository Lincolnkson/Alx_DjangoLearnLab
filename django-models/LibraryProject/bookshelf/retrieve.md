from bookshelf.models import Book

# Retrieve all the books
book = Book.objects.get("1984")
print(book)