import json

from django.views import View
from django.http  import JsonResponse

from .models import Product, ShippingFee, ShippingFee, Image, Option

class ProductDetailView(View):
    def get(self, request, product_id):

        product = Product.objects.get(id=product_id)

        images        = product.image_set.all()
        detail_images = []
        for image in images[1:]:
            detail_images.append(image.image_url)

        options      = Option.objects.filter(product=product_id)
        option_items = []
        for option in options:
            option_items.append(
                    {
                        'name'  : option.option.name,
                        'price' : option.option.price,
                        'image' : option.option.image_set.first().image_url,
                        }
                    )

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
