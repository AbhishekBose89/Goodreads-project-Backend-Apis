from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from .serializer import BookSerializer, BookReviewSerializer, UserSerializer
from .data import books
import json


# Create your views here.
book_reviews = []
users = []


class BookList(View):
    def get(self, request):
        # serialized_book = BookSerializer(books, many=True).data
        # return JsonResponse(serialized_book, safe=False)
        return JsonResponse(books, safe=False)


class BookDetails(View):
    def get(self, request, book_id):
        bookFound = None
        for book in books:
            if book["book_id"] == book_id:
                bookFound = book
                break

        if bookFound:
            serialized_book = BookSerializer(bookFound).data
            return JsonResponse(serialized_book, safe=False)
            # return JsonResponse(bookFound, safe=False)
        else:
            raise Http404("Book not found")


class BookReview(View):
    def post(self, request, book_id):
        review_data = json.loads(request.body)
        review_data["book_id"] = book_id
        review_data["review_id"] = len(book_reviews) + 1

        serialized_review_data = BookReviewSerializer(data=review_data)
        if serialized_review_data.is_valid():
            book_reviews.append(serialized_review_data.data)
            return JsonResponse(serialized_review_data.data, status=201)
        else:
            return HttpResponseBadRequest()


class Reviews(View):
    def get(self, request):
        serialized_review = BookReviewSerializer(book_reviews, many=True)
        return JsonResponse(serialized_review.data, safe=False)


class BookReviewUpdate(View):
    def put(self, request, review_id):
        review_data = json.loads(request.body)
        serialized_review = BookReviewSerializer(data=review_data)
        if serialized_review.is_valid():
            update_review = None
            for index, item in enumerate(book_reviews):
                if item["review_id"] == review_id:
                    update_review = item
                    break
            if update_review:
                book_reviews[index] = serialized_review.data
                return JsonResponse(serialized_review.data, status=200)

        return HttpResponseBadRequest()


class BookReviewDelete(View):
    def delete(self, request, review_id):
        for review in book_reviews:
            if review["review_id"] == review_id:
                book_reviews.remove(review)
                return JsonResponse({"message": "the review is deleted"}, status=200)
        return HttpResponseBadRequest()


class UserSignUp(View):
    def post(self, request):
        user_data = json.loads(request.body)
        user_data["user_id"] = len(users) + 1
        serialized_user = UserSerializer(data=user_data)
        if serialized_user.is_valid():
            users.append(serialized_user.data)
            return JsonResponse(serialized_user.data, safe=False, status=201)
        return HttpResponseBadRequest()


class UserSignIn(View):
    def post(self, request):
        user_data = json.loads(request.body)
        for user in users:
            if (
                user["email"] == user_data["email"]
                and user["password"] == user_data["password"]
            ):
                return JsonResponse("Login Successful", safe=False, status=200)
        return HttpResponseBadRequest()
