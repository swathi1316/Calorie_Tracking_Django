from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetails,Food

class Register(UserCreationForm):
    firstname = forms.CharField(label="FirstName", max_length=100)
    lastname = forms.CharField(label="LastName", max_length=100)
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["firstname", "lastname", "username", "email", "password1", "password2"]


class UserForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ["birth_date","weight","weight_goal","height","Goal","Fitness"]
        labels = {"birth_date":"Date Of Birth", "weight":"Weight","weight_goal":"Weight:Goal","height":'Height',
                  "Goal":'Goal',"Fitness":'Fitness'}


class SearchForm(forms.Form):
    scalorie = forms.CharField(label='Check Calories', max_length=100)



class CaloForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name","category"]
        labels = {"name":"Name of the Ingredient", "Category":"Meal Category"}










