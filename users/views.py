import json
import datetime

from django.views import View
from django.http  import JsonResponse

from .models import Review,User,ReviewImage

class ReviewView(View):
    def get(self,request):
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
