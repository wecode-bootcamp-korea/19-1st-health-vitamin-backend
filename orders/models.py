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
    address      = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=45)
    email        = models.EmailField()
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'shipping_informations'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'payment_methods'

class Order(models.Model):
    total                = models.PositiveIntegerField(null=True)
    paid_at              = models.DateTimeField(null=True)
    shipping_information = models.ForeignKey(ShippingInformation, on_delete=models.SET_NULL, null=True)
    user                 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method       = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL,null=True)
    coupon               = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    status               = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order   = models.ForeignKey(Order, on_delete=models.CASCADE)
    count   = models.PositiveIntegerField()
    class Meta:
        db_table = 'carts'
