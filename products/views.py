import json
import re
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models      import Menu

class MenuView(View):
    menus = Menu.objects.all()
    arr = []
    for menu in menus:
        my_dict = {
            'menu_id' : menu.id,
            'menu_name' : menu.name
        }
        arr.append(my_dict)
        return JsonResponse({'menu' : arr},status = 200)