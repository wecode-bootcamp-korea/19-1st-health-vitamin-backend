import json, datetime
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models         import Order, Cart, ShippingInformation
from users.models    import User
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
        IN_CART_STATUS_ID = 1
        data              = json.loads(request.body)
        user              = request.user
        products          = data['products']

        try:
            order = Order.objects.get(user_id=user.id, status_id=IN_CART_STATUS_ID)
            for product in products:
                order.cart_set.get(product_id=product['id']).delete()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)
    
    @user_check
    def patch(self, request):
        IN_CART_STATUS_ID = 1
        data              = json.loads(request.body)
        user              = request.user

        try:
            order = Order.objects.get(user_id=user.id, tatus_id=IN_CART_STATUS_ID)
            order.cart_set.filter(product_id=data['id']).update(count=data['count'])

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)

class OrderView(View):
    @user_check
    def get(self, request):
        IN_CART_STATUS_ID = 1
        user              = request.user

        try:
            order        = Order.objects.get(user_id=user.id, status_id=IN_CART_STATUS_ID)
            carts        = order.cart_set.all()
            product_list = [
                        {
                          'id'       : cart.product_id,
                          'count'    : cart.count,
                          'name'     : cart.product.name,
                          'price'    : cart.product.price,
                          'discount' : cart.product.discount.rate,
                          'image'    : cart.product.image_set.first().image_url
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
    def post(self, request):
        IN_CART_STATUS_ID = 1
        IS_PAID_STATUS_ID = 2
        user              = request.user
        data              = json.loads(request.body)

        try:
            if data['total'] >= 200000:
                return JsonResponse({'MESSAGE' : 'FAIL'}, status=400)

            shipping_information = data['shipping_information']

            user_shipping_information = ShippingInformation(
                    message           = shipping_information['message'],
                    name              = shipping_information['name'],
                    user_id           = user.id,
                    address           = shipping_information['address'],
                    phone_number      = shipping_information['phone_number'],
                    email             = shipping_information['email']
                    )
            user_shipping_information.save()

            order = {
                    'status_id'               : IS_PAID_STATUS_ID,
                    'paid_at'                 : datetime.datetime.now(),
                    'shipping_information_id' : user_shipping_information.id,
                    'total'                   : data['total']
                    }
            Order.objects.filter(user_id=user.id, status_id=IN_CART_STATUS_ID).update(**order)

            return JsonResponse ({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)
