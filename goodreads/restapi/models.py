from typing import Required
from django.db import models

# Create your models here.


class Book(models.Model):
    # book_id = models.AutoField(primary_key=True, default=0)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.FloatField()


class BookReview(models.Model):
    # review_id = models.AutoField(primary_key=True,default=0)
    book_id = models.IntegerField()
    user_id = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    rating = models.FloatField()


class User(models.Model):
    # user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=16)
