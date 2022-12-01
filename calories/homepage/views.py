from http.client import HTTPResponse

from django.http import JsonResponse
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Register
from django.http import HttpResponse
from .models import UserDetails

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


# Create your views here.
def usersignup(response):
    if response.method == "POST":
        form = Register(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = Register()

    return render(response, "register/register.html", {"form": form})

def homeview(request):
    return render(request,"home.html")


def SearchTemplateView(request):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = 'chicken burger'
    response = requests.get(api_url + query, headers={'X-Api-Key': 'EleW0qdfUPQTtO74is+KiA==ZnkvSqaSfxfUb2cc'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    tweet_response = {'results':response.json()}
    print(tweet_response)
    return render(request,"search/search.html", {'tweet_response':tweet_response})

def userdetailview(request):
    if request.method=="POST":
        form = UserDetails(birth_date=request.POST.get('birth_date'),weight = request.POST.get('weight'),
                           weight_goal=request.POST.get('weight_goal'), height=request.POST.get('height'),
                           Goal=request.POST.get('Goal'), Fitness =request.POST.get('Fitness')
                           )

        if form.is_valid():
            user_id = UserDetails.objects.get(pk=user_id)
            existingform = form(request.POST, instance=user_id)
            form.save()  # cleaned indenting, but would not save unless I added at least 6 characters.
            return redirect('register')
        else:
            form.save()
        return render_to_response('editbook.html', {'form': book_form}, context_instance=RequestContext(request))

    def signup_student_output(request):
        en = student(name=request.POST.get('name'), cl=request.POST.get('class'),
                     mark=request.POST.get('mark'), gender=request.POST.get('gender'))
        en.save()
        str1 = "Data inserted to student table with id:" + str(en.id)
        return render(request, 'signup_student.html', {'msg': str1})

    return render(request,"user/details.html")

