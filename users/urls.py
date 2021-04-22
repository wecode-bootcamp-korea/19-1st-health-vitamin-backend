from django.urls import path
from .views import SignUpView, SignInView,UserReviewView, WishListView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/reviews/<int:product_id>', UserReviewView.as_view()),
    path('/wishlist', WishListView.as_view())
]
