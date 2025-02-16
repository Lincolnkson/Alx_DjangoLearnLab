create command:
>>> from bookshelf.models import Book
>>> #Create a Book instance.
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()
>>> print(book)
1984

retrieve command:
>>> book = Book.objects.get("1984")
>>> print(book)
<QuerySet [<Book: 1984>]>


update command:
>>> book = Book.objects.get("1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(book)
Nineteen Eighty-Four


delete command:

>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> book = Book.objects.all()
>>> print(book)
<QuerySet []>
