# Generated by Django 3.2 on 2021-04-15 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_is_hit_product_is_best'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sub_cateory',
            new_name='sub_category',
        ),
    ]
