import json

from django.views import View
from django.http  import JsonResponse

from .models import Product, ShippingFee, ShippingFee, Image, Option

class ProductDetailView(View):
    def get(self, request, product_id):

        product = Product.objects.get(id=product_id)

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
                    'shipping_fee'  : product.shipping_fee.price,
                    'minimum_free'  : product.shipping_fee.minimum_free,
                    'discount'      : product.discount.rate,
                    'main_image'    : images.first().image_url,
                    'detail_images' : detail_images,
                    'option_items'  : option_items,
                        }
                    ]

        return JsonResponse({'result' : result}, status=200)         
