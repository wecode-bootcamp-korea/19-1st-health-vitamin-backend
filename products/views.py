import json
import datetime

from django.views import View
from django.http  import JsonResponse

from .models      import Product, ShippingFee, Image, Option, Discount, SubCategoryProduct,MainCategory
from users.models import Review,ReviewImage

class ProductDetailView(View):
    def get(self, request, product_id):
        try: 
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            if product.is_option:
                return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status=400)
            
            images = product.image_set.all()
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

class CategoryView(View):
    def get(self,request):
        try:
            categories = MainCategory.objects.all()
            category_list = [{
                'main_category_id'   : category.id,
                'main_category_name' : category.name,
                'main_category_list' : [{'category_id'  : subcategory.id,
                                         'category_name' : subcategory.name
                                        } for subcategory in category.subcategory_set.all()]
                }for category in categories]

            return JsonResponse({'category': category_list}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
    
class ProductlistView(View):
    def get(self,request,sub_category_id):
        try:
            ALL_PRODUCTS = 0
            products = Product.objects.filter(sub_category__id=sub_category_id)
            limit        = int(request.GET.get('limit', 16))
            offset       = int(request.GET.get('offset', 0))
            
            if sub_category_id == ALL_PRODUCTS:
                products = Product.objects.all()

            if not products.exists():
                return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)

            product_list = [{
                    'name'       : product.name,
                    'price'      : product.price,
                    'expired_at' : product.expired_at,
                    'is_best'    : product.is_best,
                    'discount'   : Discount.objects.get(id=product.discount_id).rate,
                    'image'      : Image.objects.filter(product_id=product.id).first().image_url,
                    'id'         : product.id
                    } for product in products if not product.is_option]
                    
            return JsonResponse({'product': product_list[offset:offset+limit]},status = 200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class ProductReviewView(View):
    def get(self,request):
        try:
            reviews = Review.objects.all().order_by('uploaded_at')[:10]
            main_page_review_list=[{
                    'review_id'         : review.id,
                    'product_name'      : review.product.name,
                    'product_image'     : review.product.image_set.all().first().image_url,
                    'user_account'      : review.user.account,
                    'user_age'          : datetime.datetime.today().year - int(str(review.user.date_of_birth)[:4]) +1,
                    'user_review'       : review.text,
                    'uploaded_at'       : review.uploaded_at,
                    'updated_at'        : review.updated_at,
                    'user_review_image' : review.reviewimage_set.get(review=review).image_url if review.reviewimage_set.filter(review=review) else None,
                    'gender'            : review.user.gender
                    } for review in reviews]

            return JsonResponse({'MAIN_PAGE_REVIEW' : main_page_review_list}, status = 200)

        except Review.DoesNotExist:
            return JsonResponse({'MESSAGE':'REVIEW_DOES_NOT_EXIST'}, status=404)

class BestProductView(View):
    def get(self,request):
        try:
            products = Product.objects.all().order_by('stock')
            best_product_list=[{
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : Discount.objects.get(id=product.discount_id).rate,
                        'image'      : Image.objects.filter(product_id=product.id).first().image_url,
                        'product_id' : product.id
                        } for product in products if product.is_best==1][:8]

            return JsonResponse({'BEST_PRODUCT' : best_product_list}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE': 'PRODUCT_DOES_NOT_EXIST'},status =404)

class HashTagView(View):
    def get(self,request):
        try:
            growth_products = SubCategoryProduct.objects.filter(sub_category=5,product__is_best=1)
            growth_product_list=[{
                        'name'       : growth_product.product.name,
                        'price'      : growth_product.product.price,
                        'discount'   : Discount.objects.get(id=growth_product.product.discount_id).rate,
                        'image'      : Image.objects.filter(product_id=growth_product.product.id).first().image_url,
                        'product_id' : growth_product.product.id 
                        } for growth_product in growth_products][:3]

            focus_on_products = SubCategoryProduct.objects.filter(sub_category=6,product__is_best=1)
            focus_on_product_list=[{
                    'name'       : focus_on_product.product.name,
                    'price'      : focus_on_product.product.price,
                    'discount'   : Discount.objects.get(id=focus_on_product.product.discount_id).rate,
                    'image'      : Image.objects.filter(product_id=focus_on_product.product.id).first().image_url,
                    'product_id' : focus_on_product.product.id
                    } for focus_on_product in focus_on_products][:3]
        
            skin_products = SubCategoryProduct.objects.filter(sub_category=1,product__is_best=1)
            skin_product_list=[{
                    'name'       : skin_product.product.name,
                    'price'      : skin_product.product.price,
                    'discount'   : Discount.objects.get(id=skin_product.product.discount_id).rate,
                    'image'      : Image.objects.filter(product_id=skin_product.product.id).first().image_url,
                    'product_id' : skin_product.product.id
                    } for skin_product in skin_products][:3]
        
            eye_products = SubCategoryProduct.objects.filter(sub_category=3,product__is_best=1)
            eye_product_list=[{
                    'name'       : eye_product.product.name,
                    'price'      : eye_product.product.price,
                    'discount'   : Discount.objects.get(id=eye_product.product.discount_id).rate,
                    'image'      : Image.objects.filter(product_id=eye_product.product.id).first().image_url,
                    'product_id' : eye_product.product.id
                    } for eye_product in eye_products][:3]

            return JsonResponse({
                'HASH_TAG_GROWTH_PRODUCT'   : growth_product_list,
                'HASH_TAG_FOCUS_ON_PRODUCT' : focus_on_product_list,
                'HASH_TAG_SKIN_PRODUCT'     : skin_product_list,
                'HASH_TAG_EYE_PRODUCT'      : eye_product_list}, status=200)
                
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE': 'PRODUCT_DOES_NOT_EXIST'},status =404)