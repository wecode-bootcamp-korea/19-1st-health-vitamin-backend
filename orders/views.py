import json

from django.views import View
from django.http import JsonResponse
from django.db import transaction

from .models import User, Order, Cart
from products.models import Product

class CartView(View):
    STATUS_IN_CARTS = 1

    @transaction.atomic
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        if not Order.objects.filter(user_id=user.id).exists():
            order = Order(status_id=STATUS_IN_CARTS, user_id=user.id)
            order.save()

        if Order.objects.get(user_id=user.id).status_id != STATUS_IN_CARTS:
            order = Order(status_id=STATUS_IN_CARTS, user_id=user.id)
            order.save()

        if Cart.objects.filter(product_id=data['id']).exists():
            count = Cart.objects.get(product_id=data['id']).count
            count += data['count']
            count.save()

        cart = Cart(
                product_id=data['id'],
                count=data['count'],
                order_id=Order.objects.get(user_id=user.id).id
                )
        cart.save()

        options = data['options']
        for option in options:
            if Cart.objects.filter(product_id=option['option_id']).exists():
                option_count = Cart.objects.get(product_id=option['option_id']).count
                option_count += option['count']
                option_count.save()

            cart = Cart(
                    product_id=option['option_id'],
                    count=option['count'],
                    order_id=Order.objects.get(user_id=user.id).id
                    )
            cart.save()

            return ({'MESSAGE' : 'SUCCESS'}, status=201)
