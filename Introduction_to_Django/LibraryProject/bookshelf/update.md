from bookshelf.models import Book

# Update the title of the created book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)