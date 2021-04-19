import json

from django.views import View
from django.http  import JsonResponse

from .models import Product, ShippingFee, ShippingFee, Image, Option, Discount, MainCategory

class ProductDetailView(View):
    def get(self, request, product_id):
        try: 
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            if product.is_option:
                return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status=400)
            
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

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)

class CategoryView(View):
    def get(self,request):
        try:
            categories = MainCategory.objects.all()
            category_list = []
            for category in categories:
                subcategorylist=[]
                subcategories = category.subcategory_set.all()
                for subcategory in subcategories:
                    subcategoryinfo = {
                        'category_id'   : subcategory.id,
                        'category_name' : subcategory.name
                    }
                    subcategorylist.append(subcategoryinfo)
                category_list.append({
                    'main_category_id'   : category.id,
                    'main_category_name' : category.name,
                    'main_category_list' : subcategorylist
                    })
            return JsonResponse({'category': category_list}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
    
class ProductlistView(View):
    def get(self,request,sub_category_id):
        try:
            ALL_PRODUCTS = 0
            products = Product.objects.filter(sub_category__id=sub_category_id)
            
            if sub_category_id == ALL_PRODUCTS:
                products = Product.objects.all()

            if not products:
                return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)

            product_list = [{
                    'name'       : product.name,
                    'price'      : product.price,
                    'expired_at' : product.expired_at,
                    'is_best'    : product.is_best,
                    'discount'   : Discount.objects.get(id=product.discount_id).rate,
                    'image'      : Image.objects.filter(product_id=product.id).first().image_url,
                    'product_id' : product.id
                    } for product in products if not product.is_option]
                    
            return JsonResponse({'product': product_list},status = 200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)



