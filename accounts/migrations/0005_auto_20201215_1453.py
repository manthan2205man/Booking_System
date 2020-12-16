# Generated by Django 3.1.4 on 2020-12-15 09:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(null=True, validators=[django.core.validators.RegexValidator(code='invalid_number', message='invalid number', regex='\\d{10}')]),
        ),
    ]
