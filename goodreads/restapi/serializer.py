from rest_framework import serializers
from .models import Book, BookReview, User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        # fields = ("book_id", "title", "author")


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
