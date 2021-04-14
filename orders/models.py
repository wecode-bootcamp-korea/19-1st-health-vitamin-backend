from django.db       import models

from users.models    import User, Coupon
from products.models import Product

class Status(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'statuses'

class ShippingInformation(models.Model):
    message      = models.CharField(max_length=100)
    name         = models.CharField(max_length=45)
    address      = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=45)
    email        = models.EmailField()
    users        = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'shipping_informations'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'payment_methods'

class Order(models.Model):
    total                 = models.PositiveIntegerField()
    paid_at               = models.DateTimeField(auto_now_add=True)
    shipping_informations = models.ForeignKey(ShippingInformation, on_delete=models.CASCADE)
    users                 = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_methods       = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL,null =True)
    coupons               = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    statuses              = models.ForeignKey(Status, on_delete=models.CASCADE)
    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    orders   = models.ForeignKey(Order, on_delete=models.CASCADE)
    count    = models.PositiveIntegerField()
    class Meta:
        db_table = 'carts'