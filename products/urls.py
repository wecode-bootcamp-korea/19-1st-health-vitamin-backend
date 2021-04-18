from django.urls import path
from .views import ProductDetailView,ProductlistView,CategoryView

urlpatterns = [
    path('/category',CategoryView.as_view()),
    path('/<int:sub_category_id>',ProductlistView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]
