import json, bcrypt, jwt, re, datetime

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import Review,User,ReviewImage,Product
from utils.decorator  import user_check
import my_settings

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        MINIMUM_PASSWORD_LENGTH = 8
        MINIMUM_ACCOUNT_LENGTH  = 5

        try:
            account       = data['account']
            division      = data['division']
            password      = data['password']
            name          = data['name']
            phone_number  = data['phone_number']
            email         = data['email']
            date_of_birth = data['date_of_birth']
            gender        = data['gender']

            email_check = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            email_check = email_check.match(email)

            if len(account) < MINIMUM_ACCOUNT_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID_ACCOUNT'}, status = 400)

            if User.objects.filter(account=account).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATE_ACCOUNT'}, status = 400)

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATE_PHONE_NUMBER'}, status = 400)

            if not email_check:
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(
                    password.encode('utf-8'), 
                    bcrypt.gensalt()
                    )

            User.objects.create(
                division      = division,
                account       = account,
                password      = hashed_password.decode('utf-8'),
                name          = name,
                phone_number  = phone_number,
                email         = email,
                gender        = gender,
                date_of_birth = date_of_birth
                )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status = 404)

            user = User.objects.get(email=email)
            hashed_password = user.password.encode('utf-8')

            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 401)

            access_token = jwt.encode({'user_id' : user.id}, my_settings.SECRET_KEY, algorithm = my_settings.ALGORITHM)

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : access_token}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

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

    #@user_check
    def post(self,request,product_id):
        try: 
            data       = json.loads(request.body)
            text       = data['text']
            product    = Product.objects.get(id=product_id) 
            #user       = request.user
            user = User.objects.get(id=28)
            image       = data.get('image',None)

            if Review.objects.filter(product=product,user=user).exists():
                return JsonResponse({'MESSAGE': 'REVIEW_CAN_WRITE_ONCE'}, status = 400)

            Review.objects.create(
                user    = user,
                product = product,
                text    = text
                )
            
            review = Review.objects.get(user=user, product=product)
            print(review)

            ReviewImage.objects.create(
                    image_url = image,
                    review    = Review.objects.get(id=review)
                )

            return JsonResponse({'MESSAGE': 'REVIEW_CREATED'}, status=201)

        #except TypeError:
        #    return JsonResponse({"MESSAGE":"TYPE_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)
        except ValueError:
            return JsonResponse({"MESSAGE":"CHECK_YOUR_VALUE"}, status= 400)

    #@user_check
    def delete(self,request,product_id):
        try:
            user    = request.user
            product = Product.objects.get(id=product_id)
            #user    = User.objects.get(id=28)
            user = User.objects.get(id=29)

            if not Review.objects.filter(product=product,user=user).exists():
                return JsonResponse({"MESSAGE": "YOUR_REVIEW_DOES_NOT_EXIST"},status=400)
        
            Review.objects.filter(product=product,user=user).delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except TypeError:
            return JsonResponse({"MESSAGE":"TYPE_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXIST"}, status=404)
        except ValueError:
            return JsonResponse({"MESSAGE":"CHECK_YOUR_VALUE"}, status= 400)
