# Generated by Django 3.2 on 2021-04-20 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_statuse_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid_at',
            field=models.DateTimeField(null=True),
        ),
    ]
