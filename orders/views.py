import json
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models         import User, Order, Cart
from products.models import Product

class CartView(View):
    @transaction.atomic
    def post(self, request):
        STATUS_IN_CART = 1

        user       = request.user
        data       = json.loads(request.body)
        product_id = data['id']
        count      = data['count']

        save_point = transaction.savepoint()

        try:
            if not Order.objects.filter(user_id=user.id).exists():
                order = Order(status_id=STATUS_IN_CART, user_id=user.id)
                order.save()

            if not Order.objects.filter(user_id=user.id, status_id=STATUS_IN_CART).exists():
                order = Order(status_id=STATUS_IN_CART, user_id=user.id)
                order.save()

            order   = Order.objects.filter(user_id=user.id, status_id=STATUS_IN_CART)
            product = order.first().cart_set.filter(product_id=product_id)

            if product.exists():
                product        = product.first()
                product.count += count
                product.save()

            else:
                cart = Cart(
                    product_id = product_id,
                    count      = count,
                    order_id   = order.first().id
                    )
                cart.save()

            options = data['options']
            for option in options:
                product_option = order.first().cart_set.filter(product_id=option['option_id'])

                if product_option.exists():
                    product_option        = product_option.first()
                    product_option.count += option['count']
                    product_option.save()

                else:
                    cart = Cart(
                        product_id = option['option_id'],
                        count      = option['count'],
                        order_id   = order.first().id
                        )
                    cart.save()

            transaction.savepoint_commit(save_point)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except JSONDecodeError:
            transaction.savepoint_rollback(save_point)
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            transaction.savepoint_rollback(save_point)
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            transaction.savepoint_rollback(save_point)
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)
