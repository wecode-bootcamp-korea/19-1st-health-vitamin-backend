import json, bcrypt

from django.http    import JsonResponse
from django.views   import View

from .models        import User


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        MINIMUM_PASSWORD_LENGTH = 8
        MINIMUM_ACCOUNT_LENGTH  = 5

        try:
            if len(data['account']) < MINIMUM_ACCOUNT_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID_ACCOUNT'}, status = 400)

            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATE_ACCOUNT'}, status = 400)

            if User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATE_PHONE_NUMBER'}, status = 400)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE' : INVALID_EMAIL}, status = 400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATE_EMAIL'}, status = 400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(
                    data['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                    )

            if data['date_of_birth'] > datetime.today():
                return JsonResponse({'MESSAGE' : 'INVALID_DATE_OF_BIRTH'}, status = 400)

            User.objects.create(
                division      = data['division']
                account       = data['account']
                password      = hashed_password.decode('utf-8')
                name          = data['name']
                phone_number  = data['phone_number']
                email         = data['email']
                gender        = data['gender']
                date_of_birth = data['date_of_birth']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)


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

            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = 'HS256')

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, 'ACCESS_TOKEN' : access_token}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
