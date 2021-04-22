from django.urls import path
<<<<<<< HEAD
from .views import SignUpView, SignInView,UserReviewView, WishlistView
=======
from .views import SignUpView, SignInView,UserReviewView, WishListView
>>>>>>> main

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/reviews/<int:product_id>', UserReviewView.as_view()),
<<<<<<< HEAD
    path('/wishlist', WishlistView.as_view()),
=======
    path('/wishlist', WishListView.as_view())
>>>>>>> main
]
