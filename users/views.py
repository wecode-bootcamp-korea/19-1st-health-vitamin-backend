import json
import datetime

from django.views import View
from django.http  import JsonResponse

from .models import Review,User,ReviewImage

class ReviewView(View):
    def get(self,request,product_id):
        try:
            reviews = Review.objects.all()
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

    @user_check
    def post(self,request):
            try: 
            data       = json.loads(request.body)
            content    = data.get('content')
            product_id = data.get('product_id')
            product    = Product.objects.get(pk=product_info)

            Review.objects.create(user=request.user, product=product_id,content=content)

            return JsonResponse({'result': 'Review Created'}, status=201)
        except TypeError:
            return JsonResponse({"message":"Type_Error"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"message":"Product_DoesNotExist"}, status=404)
    

    @user_check
    def delete(self,request,product_id):
        user = request.user
        

            

