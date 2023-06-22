from django.urls import path
from .views import (
    BookDetails,
    BookList,
    BookReview,
    BookReviewUpdate,
    BookReviewView,
    BookSearch,
    CreateBook,
    Reviews,
    BookReviewDelete,
    UserSignUp,
    UserSignIn,
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("books/", BookList.as_view(), name="book list"),
    path("books/<int:book_id>/", BookDetails.as_view(), name="book details"),
    path(
        "books/<int:book_id>/reviews/",
        csrf_exempt(BookReviewView.as_view()),
        name="book review",
    ),
    path(
        "reviews/<int:review_id>/",
        csrf_exempt(BookReviewUpdate.as_view()),
        name="book review update",
    ),
    path("books/reviews/", Reviews.as_view(), name="reviews"),
    path(
        "book/reviews/<int:review_id>/delete",
        csrf_exempt(BookReviewDelete.as_view()),
        name="delete review",
    ),
    path("users/signup/", csrf_exempt(UserSignUp.as_view()), name="user signup"),
    path("users/signin/", csrf_exempt(UserSignIn.as_view()), name="user signin"),
    path("books/create/", csrf_exempt(CreateBook.as_view()), name="create-book"),
    path("books/search/", BookSearch.as_view(), name="search-book"),
]
