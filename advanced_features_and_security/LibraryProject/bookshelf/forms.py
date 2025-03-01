from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
          class Meta:
                    model = Book
                    fields = ['title', 'author', 'publication_year']
                    labels = {
                              'title': 'Book Title',
                              'author': 'Author',
                              'publication_year': 'Publication Year'
                    }
                    help_texts = {
                              'title': 'Enter the title of the book',
                              'author': 'Enter the author of the book',
                              'publication_year': 'Enter the publication year of the book'
                    }
                    error_messages = {
                              'title': {
                                        'required': 'Please enter the title of the book'
                              },
                              'author': {
                                        'required': 'Please enter the author of the book'
                              },
                              'publication_year': {
                                        'required': 'Please enter the publication year of the book'
                              }
                    }

          def clean_title(self):
                    title = self.cleaned_data['title']
                    if len(title) < 5:
                              raise forms.ValidationError('Title should be at least 5 characters long')
                    return title

          def clean_author(self):
                    author = self.cleaned_data['author']
                    if len(author) < 5:
                              raise forms.ValidationError('Author should be at least 5 characters long')
                    return author

          def clean_publication_year(self):
                    publication_year = self.cleaned_data['publication_year']          
                  