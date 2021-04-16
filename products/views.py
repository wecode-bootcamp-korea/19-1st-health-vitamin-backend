import json

from django.views import View
from django.http  import JsonResponse

from .models import Product, ShippingFee, ShippingFee, Image, Option

class ProductDetailView(View):
    def get(self, request, product_id):

        try: 

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE':'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            if product.is_option:
                return JsonResponse({'MESSAGE':'NOT_FOUND'}, status=404)
            
            images        = product.image_set.all()
            detail_images = [image.image_url for image in images[1:]]

            options      = Option.objects.filter(product=product_id)
            option_items = [
                {
                    'name'  : option.option.name,
                    'price' : option.option.price,
                    'image' : option.option.image_set.first().image_url
                    }
                for option in options
                ]

            result = [
                {
                    'name'          : product.name,
                    'price'         : product.price,
                    'detail'        : product.detail,
                    'shipping_fee'  : product.shipping_fee.price,
                    'minimum_free'  : product.shipping_fee.minimum_free,
                    'discount'      : product.discount.rate,
                    'main_image'    : images.first().image_url,
                    'detail_images' : detail_images,
                    'option_items'  : option_items,
                        }
                    ]

            return JsonResponse({'RESULT' : result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
