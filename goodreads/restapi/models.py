from pickle import TRUE
from django.db import models

# Create your models here.


class Book(models.Model):
    book_id = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BookReview(models.Model):
    book_id = models.IntegerField()
    review_id = models.IntegerField()
    user_id = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2)


class User(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=16)
