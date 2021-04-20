from django.db       import models

from products.models import Product

class User(models.Model):
    account       = models.CharField(max_length=50)
    password      = models.CharField(max_length=1000)
    name          = models.CharField(max_length=10)
    email         = models.EmailField(max_length=200)
    phone_number  = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    division      = models.BooleanField(default=0)
    gender        = models.BooleanField(default=0)
    product       = models.ManyToManyField(Product, through='Like')
    class Meta:
        db_table = 'users'

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'likes'

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, through='UserCoupon')
    class Meta:
        db_table = 'coupons'

class UserCoupon(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_coupons'

class Review(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text        = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review    = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_url = models.URLField(null=True)
    class Meta:
        db_table = 'review_images'
