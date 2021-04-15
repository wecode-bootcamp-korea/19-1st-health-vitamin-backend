import json

from django.http    import JsonResponse
from django.views   import View

from .models        import User


class SignUpView(View):
    def post(self, request):
    MINIMUM_PASSWORD_LENGTH = 8
    MINIMUM_ACCOUNT_LENGTH = 5

        try:
            data = json.loads(request.body)

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

            if data['date_of_birth'] > datetime.today():
                return JsonResponse({'MESSAGE' : 'INVALID_DATE_OF_BIRTH'}, status = 400)

            User.objects.create(
                division      = data['division']
                account       = data['account']
                password      = data['password']
                name          = data['name']
                phone_number  = data['phone_number']
                email         = data['email']
                gender        = data['gender']
                date_of_birth = data['date_of_birth']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
