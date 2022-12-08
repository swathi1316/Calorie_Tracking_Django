# Generated by Django 3.0.2 on 2022-12-05 23:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0009_delete_userdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField()),
                ('Gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], max_length=50, verbose_name='Gender')),
                ('weight', models.DecimalField(decimal_places=1, default=1, max_digits=4, validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(1)])),
                ('weight_goal', models.DecimalField(decimal_places=1, default=1, max_digits=4, validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(1)])),
                ('height', models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('Goal', models.CharField(choices=[('maintain_weight', 'maintain_weight'), ('loose_weight', 'loose_weight'), ('gain_weight', 'gain_weight')], max_length=50, verbose_name='Goal')),
                ('Fitness', models.CharField(choices=[('no_exercise', 'no_exercise'), ('mild_exercise', 'mild_exercise'), ('regular_exercise', 'regular_exercise')], max_length=50, verbose_name='Fitness')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
