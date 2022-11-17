from django.http import JsonResponse
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Register

import os
import requests
from requests import request

# class HomepageView(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html'
#     login_url = '/auth/login/'
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


# Create your views here.
def UserSignup(response):
    if response.method == "POST":
        form = Register(response.POST)
        if form.is_valid():
            form.save()
            return redirect("base.html")
    else:
        form = Register()

    return render(response, "register.html", {"form": form})
