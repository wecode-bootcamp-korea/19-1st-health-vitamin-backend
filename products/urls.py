from django.urls import path
from .views import ProductDetailView,ProductlistView,CategoryView,MainReviewView,MainBestProductView,HashTagView

urlpatterns = [
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/category',CategoryView.as_view()),
    path('/<int:sub_category_id>',ProductlistView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/main/review',MainReviewView.as_view()),
    path('/main/best',MainBestProductView.as_view()),
    path('/main/hashtag',HashTagView.as_view())
]
