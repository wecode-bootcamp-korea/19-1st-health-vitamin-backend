import jwt
import json
import requests

from django.http           import JsonResponse
from users.models          import User

import my_settings

def user_check(func):
    def wrapper(self,request,*args, **kwargs):
    
        try:
            print(2)
            access_token = request.headers.get('Authorization', None)          
            payload = jwt.decode(access_token, my_settings.SECRET_KEY, algorithms=my_settings.ALGORITHM)
            user = User.objects.get(id=payload['user_id'])                 
            request.user = user                                     

        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({'MESSAGE' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:                                           
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
