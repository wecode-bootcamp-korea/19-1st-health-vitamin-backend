# Generated by Django 3.2 on 2021-04-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_type_user_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewimage',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
