import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_health_vitamin_backend.settings")
django.setup()

from products.models import *
from users.models import *
from orders.models import *

# CSV_PATH_PRODUCTS = './main_categories.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         name=row[0]
#         MainCategory.objects.create(
#           name = name
#         )

# CSV_PATH_PRODUCTS = './sub_categories.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         name=row[0]
#         main_category=MainCategory.objects.get(id=row[1]) 
#         SubCategory.objects.create(
#           name=name,
#           main_category=main_category
#         )


# CSV_PATH_PRODUCTS = './discounts.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         rate=row[0]
#         Discount.objects.create(
#           rate=rate
#         )


# CSV_PATH_PRODUCTS = './shipping_fees.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         price=row[0]
#         minimum_free=row[1]
#         ShippingFee.objects.create(
#           price=price,
#           minimum_free=minimum_free
#         )


# CSV_PATH_PRODUCTS = './products.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         name= row[0]
#         price= row[1]
#         detail= row[2]
#         stock= row[3]
#         expired_at= row[4]
#         is_best= row[5]
#         is_option= row[6]
#         discount = Discount.objects.get(id=row[7])
#         shipping_fee = ShippingFee.objects.get(id=row[8])
#         Product.objects.create(
#           name = name, 
#           price = price, 
#           detail = detail,
#           stock = stock,
#           expired_at = expired_at, 
#           is_best = is_best, 
#           is_option = is_option, 
#           discount=discount,
#           shipping_fee=shipping_fee
#           )

# CSV_PATH_PRODUCTS = './sub_category_products.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         product=Product.objects.get(id=row[0])
#         sub_category=SubCategory.objects.get(id=row[1])
#         SubCategoryProduct.objects.create(
#           product=product,
#           sub_category=sub_category
#         )


# CSV_PATH_PRODUCTS = './images.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         image_url=row[0]
#         product=Product.objects.get(id=row[1])
#         Image.objects.create(
#           image_url=image_url,
#           product=product
#         )

# CSV_PATH_PRODUCTS = './users.csv'
# with open(CSV_PATH_PRODUCTS) as in_file:
#   data_reader = csv.reader(in_file)
#   next(data_reader, None)
#   for row in data_reader:
#         account= row[0]
#         password= row[1]
#         name= row[2]
#         email= row[3]
#         phone_number= row[4]
#         date_of_birth= row[5]
#         division= row[6]
#         gender= row[7]
#         User.objects.create(
#           account=account,
#           password=password,
#           name=name,
#           email=email,
#           phone_number=phone_number,
#           date_of_birth=date_of_birth,
#           division=division,
#           gender=gender
#         )

CSV_PATH_PRODUCTS = './reviews.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
  data_reader = csv.reader(in_file)
  next(data_reader, None)
  for row in data_reader:
        text=row[0]
        product=Product.objects.get(id=row[1])
        user=User.objects.get(id=row[2])
        Review.objects.create(
          text=text,
          product=product,
          user=user
        )



        


