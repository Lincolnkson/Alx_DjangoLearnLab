from bookshelf.models import Book

# Retrieve all the books
book = Book.objects.all()
print(book)