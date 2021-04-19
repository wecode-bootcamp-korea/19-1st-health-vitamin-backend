import json, bcrypt, jwt, re

from django.http    import JsonResponse
from django.views   import View

from .models        import User
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
            print('keyErr')
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
