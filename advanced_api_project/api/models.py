from django.db import models

#The purpose of this model is to create a DB table that will store data on the Authors
class Author(models.Model):
          name = models.CharField(max_length=100)

          def __str__(self):
                    return self.name
 #The purpose of this model is to create a DB table that will store data ob the Books         
class Book(models.Model):
          title = models.CharField(max_length=200)
          publication_year = models.IntegerField()
          author = models.ForeignKey(Author, on_delete=models.CASCADE)

          def __str__(self):
                    return self.title
