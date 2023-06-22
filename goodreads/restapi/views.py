from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.views import View
from .serializer import BookSerializer, BookReviewSerializer, UserSerializer
from .data import books
import json
from .models import *

# Create your views here.
book_reviews = []
users = []


# Get all books from db
class BookList(View):
    def get(self, request):
        book_data = Book.objects.all()
        serialized_book = BookSerializer(book_data, many=True).data
        return JsonResponse(serialized_book, safe=False)


#  Create a book in db
class CreateBook(View):
    def post(self, request):
        data = json.loads(request.body)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            Book.objects.create(**data)
            return JsonResponse(serializer.data, safe=False, status=201)
        return JsonResponse(serializer.errors, safe=False)


# Get a single book  by id from db
class BookDetails(View):
    def get(self, request, book_id):
        try:
            found_book = Book.objects.get(id=book_id)
            if found_book:
                return JsonResponse(
                    BookSerializer(found_book).data, status=200, safe=False
                )
        except Exception as e:
            return HttpResponseBadRequest(str(e))


# Get a single book search by name from db
class BookSearch(View):
    def get(self, request):
        query = request.GET.get("query")
        try:
            books = Book.objects.filter(title=query)
            # books=Book.objects.filter(title=query).values()
            # if books:
            #     return JsonResponse(list(books),status=200,safe=False)
            if books:
                serialized_books = []
                for book in books:
                    serialized_books.append(BookSerializer(book).data)

                return JsonResponse(serialized_books, status=200, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


# Add a review for a particular book in db
class BookReviewView(View):
    def post(self, request, book_id):
        review_data = json.loads(request.body)
        review_data["book_id"] = book_id
        serialized_data = BookReviewSerializer(data=review_data)
        try:
            if serialized_data.is_valid():
                BookReview.objects.create(**review_data)
                return JsonResponse(serialized_data.data, status=201, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


#  Get all reviews from db
class Reviews(View):
    def get(self, request):
        review_data = BookReview.objects.all()
        serialized_review = BookReviewSerializer(review_data, many=True)
        return JsonResponse(serialized_review.data, safe=False)


# update the review in db
class BookReviewUpdate(View):
    def put(self, request, review_id):
        review_data = json.loads(request.body)
        serialized_review = BookReviewSerializer(data=review_data)
        try:
            if serialized_review.is_valid():
                review = BookReview.objects.get(id=review_id)
                for key, value in review_data.items():
                    setattr(review, key, value)
                    review.save()
                return JsonResponse(serialized_review.data, status=200)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


# Delete the review from db
class BookReviewDelete(View):
    def delete(self, request, review_id):
        # delete_review = BookReview.objects.delete(id=review_id)
        delete_review = BookReview.objects.get(id=review_id).delete()
        # delete_review.delete()
        serialized_review = BookReviewSerializer(delete_review, many=True)
        return JsonResponse({"message": "the review is deleted"}, status=200)


# register user in db
class UserSignUp(View):
    def post(self, request):
        user_data = json.loads(request.body)
        serialized_user = UserSerializer(data=user_data)
        try:
            if serialized_user.is_valid():
                User.objects.create(**user_data)
                return JsonResponse(serialized_user.data, safe=False, status=201)
        except:
            return JsonResponse(serialized_user.errors, safe=False)


# login user from db
class UserSignIn(View):
    def post(self, request):
        user_data = json.loads(request.body)
        user_data.pop("name", None)
        serialized_user = UserSerializer(data=user_data)
        try:
            if serialized_user.is_valid():
                User.objects.get(
                    email=user_data["email"], password=user_data["password"]
                )
                return JsonResponse("Login Successful", safe=False, status=200)
            else:
                return JsonResponse(serialized_user.errors, safe=False, status=400)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
