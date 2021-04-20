import json
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models         import User, Order, Cart
from products.models import Product, ShippingFee
from utils.decorator import user_check

class CartView(View):
    @user_check
    def post(self, request):
        IN_CART_STATUS_ID = 1
        user              = request.user
        data              = json.loads(request.body)
        products          = data['products']

        try:
            with transaction.atomic():
                order, created = Order.objects.get_or_create(user_id = user.id, status_id = IN_CART_STATUS_ID)

                for product in products:
                    if Cart.objects.filter(order_id  = order.id, product_id = product['product_id']).exists():
                        cart        = Cart.objects.get(order_id = order.id, product_id = product['product_id'])
                        cart.count += product['count']
                    else:
                        cart = Cart(order_id = order.id, product_id=product['product_id'], count = product['count'])
                    cart.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)

    @user_check
    def get(self, request):
        IN_CART_STATUS_ID = 1
        user              = request.user

        try:
            if not Order.objects.filter(user_id=user.id, status_id=IN_CART_STATUS_ID).exists():
                return JsonResponse({'MESSAGE' : 'NO_PRODUCTS_IN_CART'},status=400)

            order = Order.objects.get(user_id=user.id, status_id=IN_CART_STATUS_ID)
            carts = order.cart_set.all()
            
            product_list = [
                {
                    'id'       : cart.product_id,
                    'count'    : cart.count,
                    'name'     : cart.product.name,
                    'price'    : cart.product.price,
                    'discount' : cart.product.discount.rate,
                    'image'    : cart.product.image_set.first().image_url,
                    }
                for cart in carts]

            shipping_fee = [
                {
                    'shipping_fee' : ShippingFee.objects.get(id=1).price,
                    'minimum_free' : ShippingFee.objects.get(id=1).minimum_free
                    }
                ]

            return JsonResponse(
                {
                    'MESSAGE'      : 'SUCCESS',
                    'PRODUCT_LIST' : product_list,
                    'SHIPPING_FEE' : shipping_fee},
                    status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)

    @user_check
    def delete(self, request):
        data     = json.loads(request.body)
        user     = request.user
        products = data['products']

        try:
            order = Order.objects.get(user_id=user.id, status_id=1)
            for product in products:
                order.cart_set.get(product_id=product['id']).delete()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)
