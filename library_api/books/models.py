from django.db import models
from django.contrib.auth.models import User
from authors.models import Author 


class Book(models.Model):
    title = models.CharField(max_length=255,  db_index=True) # indexing it will help in calcualting recomendation
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_index=True) # indexing it will help in calcualting recomendation
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')
