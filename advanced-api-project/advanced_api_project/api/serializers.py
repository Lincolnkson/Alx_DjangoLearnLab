import datetime
from rest_framework import serializers
from .models import Book, Author

"""
The puspose of the BookSerializer is to serialize all fields of the Book model.
Within the AuthorSerializer, the books are grouped according to the author. Meaning the bookSerializer is nested with the AuthorSerializer.
"""
class BookSerializer(serializers.ModelSerializer):

          class Meta:
                    model = Book
                    fields = '__all__'
          
          #Adding custom validation to the BookSerializer to ensure the publication_year is not in the future.
          def validate(self, data):
                    if data["publication_year"] > datetime.now().year:
                              raise serializers.ValidationError("The publication_year can not be a future year")
                    return data
          
          def __str__(self):
                  return super().__str__()

#The purpose of the AuthorSerializer is to serialize all fields of the Author model and to ensure related books are grouped.
class AuthorSerializer(serializers.ModelSerializer):
        books = BookSerializer(many=True, read_only=True)

        class Meta:
                model = Author
                fields = ['name', 'books']

        def __str__(self):
                return super().__str__()
