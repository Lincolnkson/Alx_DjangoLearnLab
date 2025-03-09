from django.db import models

# define a Book model with basic fields such as title (a CharField) and author (a CharField).
class Book(models.Model):
          title = models.CharField(max_length=50)
          author = models.CharField(max_length=50)

          def __str__(self):
                  return f"Title: {Book.title} | Author: {Book.author}"
