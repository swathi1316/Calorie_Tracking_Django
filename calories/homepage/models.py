from django.conf import settings
from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
class UserDetails(models.Model):
    goal = (
        ("maintain_weight", "maintain_weight"),
        ("loose_weight", "loose_weight"),
        ("gain_weight", "gain_weight"),
    )

    exercise = (
        ("no_exercise", "no_exercise"),
        ("mild_exercise", "mild_exercise"),
        ("regular_exercise", "regular_exercise"),
    )
    birth_date = models.DateField()
    weight = models.DecimalField(
        default=1,
        validators=[MaxValueValidator(300), MinValueValidator(1)],
        decimal_places=1,
        max_digits=4,
     )

    weight_goal = models.DecimalField(
        default=1,
        validators=[MaxValueValidator(300), MinValueValidator(1)],
        decimal_places=1,
        max_digits=4,
    )
    height = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)],
        decimal_places=1,
        max_digits=3,
     )
    Goal = models.CharField("Goal", max_length=50,
                                choices=goal)
    Fitness = models.CharField("Fitness", max_length=50,
                            choices=exercise)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        primary_key= True,
        on_delete=models.CASCADE)

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)


class Category(models.TextChoices):
    BREAKFAST = "breakfast", "breakfast"
    LUNCH = "lunch", "lunch"
    DINNER = "dinner", "dinner"
    SNACKS = "snacks", "snacks"

class Food(models.Model):
    name = models.CharField("Name of Cheese", max_length=255)
    category = models.CharField("Category", max_length=20,
                                choices=Category.choices, default=Category.BREAKFAST)

    f_calories = AutoSlugField("Total_Calories",
                         unique=True, always_update=False, populate_from="name")

    serving_size = models.DecimalField(max_digits=6,decimal_places=2)
    fat = models.DecimalField(max_digits=6,decimal_places=2)
    protein = models.DecimalField(max_digits=6,decimal_places=2)
    carbs = models.DecimalField(max_digits=6,decimal_places=2)
    cholestrol = models.DecimalField(max_digits=6,decimal_places=2)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

# Create your models here.max_digits=5,
