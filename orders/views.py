import json

from django.views import View
from django.http import JsonResponse

from .models import User, Order, Cart
from products.models import Product

class CartView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not Order.objects.filter(user_id=request.user.id).exists():
            Order.objects.create(statuse_id=1, user_id=request.user.id)

        if Order.objects.get(user_id=request.user.id).statuse_id !=1:
            Order.objects.create(statuse_id=1, user_id=request.user.id)

        if Cart.objects.filter(product_id=data['id']).exists():
            count = Cart.objects.get(product_id=data['id']).count
            count += data['count']
            count.save()

        Cart.objects.create(
                product_id=data['id'],
                count=data['count'],
                order_id=Order.objects.get(user_id=request.user.id).id
                )

        options = data['options']
        for option in options:
            if Cart.objects.filter(product_id=option['option_id']).exists():
                option_count = Cart.objects.get(product_id=option['option_id']).count
                option_count += option['count']
                option_count.save()

            Cart.objects.create(
                    product_id=option['option_id'],
                    count=option['count'],
                    order_id=Order.objects.get(user_id=request.user.id).id
                    )

            return ({'MESSAGE' : 'SUCCESS'}, status=201)
