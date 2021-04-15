import json

from django.http    import JsonResponse
from django.views   import View

from .models        import User


class SignUpView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            division      = data['division']
            account       = data['account']
            password      = data['password']
            name          = data['name']
            phone_number  = data['phone_number']
            email         = data['email']
            gender        = data['gender']
            date_of_birth = data['date_of_birth']

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
