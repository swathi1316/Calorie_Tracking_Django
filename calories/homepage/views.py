from http.client import HTTPResponse

from django.http import JsonResponse
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Register
from .forms import UserForm
from .forms import User,SearchForm
from django.http import HttpResponse
from .models import UserDetails
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import formats

import os
import requests
from requests import request

# class HomepageView(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html'
#     login_url = '/auth/registration/'
#     redirect_field_name = 'redirect_to'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['context_var'] = 'Context Data!'
#
#         return context
#
#     def post(request, *args, **kwargs):
#         url = "https://api.edamam.com/api/nutrition-data"
#
#         querystring = {"api_id": "daf89bdc", "app_key": "2b1c534692ddd49857dd8f4c53e6aa6e", 'nutrition-type': 'logging',
#                        "ingr": "apple"}
#         headers = {
#             "api_id": "daf89bdc", "app_key": "2b1c534692ddd49857dd8f4c53e6aa6e"
#         }
#         # response = requests.get(url, headers=headers,params=querystring)
#         response = requests.get(url, headers=headers, params=querystring)
#         print(response)
#         print(response)
#         calorie_response = {"result": response.json()}
#         return JsonResponse(calorie_response)
#
#
#     def context_function(self):
#         return 'Context Function Return!'



from django.shortcuts import render, redirect
from .forms import Register
from django.core.exceptions import ObjectDoesNotExist

user = get_user_model()


# Create your views here.
def usersignup(response):
    print(response.method)
    if response.method == "POST":
        form = Register(response.POST)
        if form.is_valid():
            form.save()
            return redirect('details')
    else:
        form = Register()

    return render(response, "register/register.html", {"form": form})

def homeview(request):
    return render(request,"home.html")



def SearchTemplateView(request):
    print(request.method)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['scalorie']
            api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
            query = search_field
            print(query)
            response = requests.get(api_url + query, headers={'X-Api-Key': 'EleW0qdfUPQTtO74is+KiA==ZnkvSqaSfxfUb2cc'})
            if response.status_code == requests.codes.ok:
                print(response.text)
            else:
                print("Error:", response.status_code, response.text)

            tweet_response = {'results':response.json()}
            print(tweet_response)
            return render(request,"search/search.html",{'tweet_response':tweet_response})
    else:
        form = SearchForm()
    return render(request, "search/search.html", {"form": form})



def userdetailview(response):
    if response.method == "POST":
        username = response.user.id
        form = UserForm(response.POST)
        if form.is_valid():
            if UserDetails.objects.filter(creator=username).exists():
                form.owner = username
                form.save()
                return redirect('search')
            else:
                form.save()
                return redirect('home')
    else:
        form = UserForm()
    return render(response, "user/details.html", {"form": form})
    # if request.method=="POST":
    #     username = request.user.id
    #     print(username)
    #     form = UserDetails(birth_date=request.POST.get('birth_date'),weight = request.POST.get('weight'),
    #                        weight_goal=request.POST.get('weight_goal'), height=request.POST.get('height'),
    #                        Goal=request.POST.get('Goal'), Fitness =request.POST.get('Fitness')
    #                        or None)
    #     form.birth_date = formats.date_format(form.birth_date, "SHORT_DATETIME_FORMAT")
    #     # form = UserDetails(request.POST or None)
    #     print(request.POST)
    #     if UserDetails.objects.filter(creator=username).exists():
    #         form.owner = username
    #         form.save()
    #         return redirect('home')
    #     else:
    #         form.save()
    #         return redirect('home')
    # return render(request,'user/details.html')
    #
    # # def signup_student_output(request):
    # #     en = student(name=request.POST.get('name'), cl=request.POST.get('class'),
    # #                  mark=request.POST.get('mark'), gender=request.POST.get('gender'))
    # #     en.save()
    # #     str1 = "Data inserted to student table with id:" + str(en.id)
    # #     return render(request, 'signup_student.html', {'msg': str1})
    # #
    # # return render(request,"user/details.html")

