# Generated by Django 3.2 on 2021-04-17 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='statuse',
            new_name='status',
        ),
    ]
