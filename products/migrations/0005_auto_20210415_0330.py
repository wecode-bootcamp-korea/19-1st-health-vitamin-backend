# Generated by Django 3.1.7 on 2021-04-15 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210415_0311'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubCategory_Product',
            new_name='SubCategoryProduct',
        ),
    ]
