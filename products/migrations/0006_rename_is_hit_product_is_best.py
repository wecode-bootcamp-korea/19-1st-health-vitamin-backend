# Generated by Django 3.2 on 2021-04-15 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210415_0330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_hit',
            new_name='is_best',
        ),
    ]
