import json

from django.views import View
from django.http  import JsonResponse

from .models import Product, ShippingFee, ShippingFee, Image, Option

class ProductDetailView(View):
    def get(self, request, product_id):
        try: 
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            if product.is_option:
                return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status=400)
            
            images        = product.image_set.all()
            detail_images = [
                    {
                        'image_id'  : image.id,
                        'image_url' : image.image_url 
                        }
                    for image in images]

            options      = Option.objects.filter(product=product_id)
            option_items = [
                {
                    'id'        : option.option.id,
                    'name'      : option.option.name,
                    'price'     : option.option.price,
                    'stock'     : option.option.stock,
                    'image_id'  : option.option.image_set.first().id,
                    'image_url' : option.option.image_set.first().image_url
                    }
                for option in options
                ]

            result = [
                {
                    'id'            : product.id,
                    'name'          : product.name,
                    'price'         : product.price,
                    'stock'         : product.stock,
                    'detail'        : product.detail,
                    'shipping_fee'  : product.shipping_fee.price,
                    'minimum_free'  : product.shipping_fee.minimum_free,
                    'discount'      : product.discount.rate,
                    'detail_images' : detail_images,
                    'option_items'  : option_items,
                        }
                    ]

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)



