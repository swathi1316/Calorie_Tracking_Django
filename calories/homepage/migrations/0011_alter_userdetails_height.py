# Generated by Django 3.2.12 on 2022-12-14 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='height',
            field=models.IntegerField(default=120, validators=[django.core.validators.MaxValueValidator(210), django.core.validators.MinValueValidator(120)]),
        ),
    ]
