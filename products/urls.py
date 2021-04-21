from django.urls import path
from .views import ProductDetailView,ProductlistView,CategoryView,ProductReviewView,BestProductView,HashTagView

urlpatterns = [
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/category',CategoryView.as_view()),
    path('/<int:sub_category_id>',ProductlistView.as_view()),
    path('/main-review',ProductReviewView.as_view()),
    path('/main-best',BestProductView.as_view()),
    path('/main-hashtag',HashTagView.as_view())
]