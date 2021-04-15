from django.urls import path
from products.views import MenuView

urlpatterns = [
    path('',MenuView.as_view())
]

