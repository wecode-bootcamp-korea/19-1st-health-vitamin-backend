from django.db    import models

class MainCategory(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete= models.SET_NULL, null=True)
    name          = models.CharField(max_length=45)
    class Meta:
        db_table = 'sub_categories'

class Discount(models.Model):
    rate = models.PositiveIntegerField()
    class Meta:
        db_table = 'discounts'

class ShippingFee(models.Model):
    price        = models.PositiveIntegerField()
    minimum_free = models.PositiveIntegerField()
    class Meta:
        db_table = 'shipping_fees'

class Product(models.Model):
    name         = models.CharField(max_length=45)
    price        = models.PositiveIntegerField()
    detail       = models.TextField()
    stock        = models.PositiveIntegerField()
    expired_at   = models.DateField()
    is_best      = models.BooleanField(default=0)
    is_option    = models.BooleanField(default=0)
    discount     = models.ForeignKey(Discount,on_delete=models.SET_NULL, null=True)
    shipping_fee = models.ForeignKey(ShippingFee, on_delete=models.SET_NULL, null=True)
    sub_category  = models.ManyToManyField(SubCategory,through='SubCategoryProduct')
    option       = models.ManyToManyField('self',through='Option',symmetrical=False)
    class Meta:
        db_table = 'products'

class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='main_product', null=True)
    option  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='main_product_option')
    class Meta:
        db_table = 'options'

class SubCategoryProduct(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'sub_category_products'

class Image(models.Model):
    product   = models.ForeignKey(Product,on_delete=models.CASCADE)
    image_url = models.URLField()
    class Meta:
        db_table = 'images'








    


