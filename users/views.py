import json
import datetime

from django.views import View
from django.http  import JsonResponse
from django.db.models import Q

from .models import Review,User,ReviewImage,Product

class ReviewView(View):
    def get(self,request,product_id):
        try:
            reviews = Review.objects.filter(product=product_id)

            if not reviews.exists():
                return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'},status = 404)

            review_list = []
            for review in reviews:
                user_review_image_list=[]
                for image in review.reviewimage_set.all():
                    user_review_image_list.append({
                        'review_image_id' : image.id,
                        'review_image'    : image.image_url
                    })
 
                review_list.append({
                    'review_id'         : review.id,
                    'product_name'      : review.product.name,
                    'product_image'     : review.product.image_set.all().first().image_url,
                    'user_account'      : review.user.account,
                    'user_age'          : datetime.datetime.today().year - int(str(review.user.date_of_birth)[:4]) +1,
                    'user_review'       : review.text,
                    'uploaded_at'       : review.uploaded_at,
                    'updated_at'        : review.updated_at,
                    'user_review_image' : user_review_image_list,
                    'gender'            : review.user.gender
                })
            return JsonResponse({'REVIEW' : review_list},status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'},status = 400)

    # @user_check
    def post(self,request,product_id):
        try: 
            data       = json.loads(request.body)
            text       = data['text']
            product    = Product.objects.get(id=product_id) 
            #user       = request.user
            user = User.objects.get(id=28)

            if Review.objects.filter(product=product,user=user).exists():
                return JsonResponse({'MESSAGE': 'REVIEW_CAN_WRITE_ONCE'}, status = 400)

            Review.objects.create(
                user    = user,
                product = product,
                text    = text)

            return JsonResponse({'MESSAGE': 'REVIEW_CREATED'}, status=201)

        except TypeError:
            return JsonResponse({"MESSAGE":"TYPE_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)
        except ValueError:
            return JsonResponse({"MESSAGE":"CHECK_YOUR_VALUE"}, status= 400)

     # @user_check
    def delete(self,request,product_id):
        try:
             # user    = request.user
            product = Product.objects.get(id=product_id)
            user    = User.objects.get(id=28)

            if not Review.objects.filter(product=product,user=user):
                return JsonResponse({"MESSAGE": "YOUR_REVIEW_DOES_NOT_EXIST"},status=400)
        
            Review.objects.filter(product=product,user=user).delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except TypeError:
            return JsonResponse({"MESSAGE":"TYPE_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)
        except ValueError:
            return JsonResponse({"MESSAGE":"CHECK_YOUR_VALUE"}, status= 400)
        
        

        

            

