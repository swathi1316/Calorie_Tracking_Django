from django.contrib import admin
from .models import UserDetails
from .models import Category
from .models import Food

admin.site.register(UserDetails)
admin.site.register(Food)

