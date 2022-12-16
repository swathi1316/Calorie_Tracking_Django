import datetime
import decimal
from random import randint

from django.contrib.auth import authenticate,logout
from http.client import HTTPResponse

from django.http import JsonResponse
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Register
from .forms import UserForm
from .forms import User, SearchForm, CaloForm
from django.http import HttpResponse
from .models import Food, UserDetails
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import formats
from django.utils import timezone
from datetime import date
from datetime import datetime

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


### LogOut

def logout_view(request):
    logout(request)
    return redirect('home')


def ApiView(param):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = param
    #print(query)
    response = requests.get(api_url + query, headers={'X-Api-Key': 'EleW0qdfUPQTtO74is+KiA==ZnkvSqaSfxfUb2cc'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    tweet_response = {'results': response.json()}
    print(tweet_response)
    return tweet_response

def FitnessApi(param):
    import requests

    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    # querystring = {"age": "25", "gender": "male", "height": "180", "weight": "70", "activitylevel": "level_1"}
    print("query:",param)

    querystring = param

    headers = {
        "X-RapidAPI-Key": "7be9411e0dmshf598957837a3cf1p128d37jsncb48ee01a6ae",
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    tweet_response = {'results': response.json()}
    return tweet_response

def SearchTemplateView(request):
    #print(request.method)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['scalorie']
            calo_response = ApiView(search_field)
            return render(request,"search/search.html",{'tweet_response':calo_response,'form':form})
    else:
        form = SearchForm()
    return render(request, "search/search.html", {"form": form})



def userdetailview(response):
    if response.method == "POST":
        username = response.user
        # user_details = UserDetails.objects.get(creator=username)
        form = UserForm(response.POST)
        print(form)
        if form.is_valid():
            if UserDetails.objects.filter(creator=username).exists():
                UserDetails.objects.filter(creator=username).update(birth_date=form.cleaned_data["birth_date"],
                                                                Gender=form.cleaned_data['Gender'],weight=form.cleaned_data['weight'],weight_goal=form.cleaned_data['weight_goal'],
                                                                       height= form.cleaned_data['height'],Goal=form.cleaned_data["Goal"],Fitness=form.cleaned_data["Fitness"])
                return redirect('tracking')
            else:
                user = UserDetails()
                user.birth_date = form.cleaned_data["birth_date"]
                user.Gender = form.cleaned_data['Gender']
                user.weight = form.cleaned_data['weight']
                user.weight_goal = form.cleaned_data['weight_goal']
                user.height = form.cleaned_data['height']
                user.Goal = form.cleaned_data['Goal']
                user.Fitness = form.cleaned_data['Fitness']
                user.creator = username
                user.save()
                return redirect('tracking')
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
@login_required()
def UserTracking(request):
    print("user:",request.user)
    username = request.user
    if request.method == "POST":
        form = CaloForm(request.POST)
        username = request.user
        if form.is_valid():
            ing_name = form.cleaned_data['name']
            foodlist = ing_name.split()
            foodname = foodlist[1]
            print("foodname:",foodname)
            quantity = foodlist[0]
            #print(ing_name)
            category = form.cleaned_data['category']
            #print(category)
            food_respons =ApiView(ing_name)
            # print(ing_reponse)
            food_response = food_respons['results']['items']
            # print(len(ing_response))
            # print(ing_response)
            food = Food()
            update_food = Food.objects.filter(creator=username).filter(created=date.today()).filter(category=category).filter(name=foodname)
            for nutrientdict in food_response:
                if update_food.exists():
                    print("food exists")
                    update_food.update(serving_size=nutrientdict['serving_size_g'],f_calories=nutrientdict['calories'],fat=nutrientdict['fat_total_g'],
                                protein=nutrientdict['protein_g'],carbs=nutrientdict['carbohydrates_total_g'],cholesterol=nutrientdict['cholesterol_mg'])
                    break
                else:
                    print("new food exists")
                    food.name = nutrientdict['name']
                    food.category = category
                    food.f_calories = nutrientdict['calories']
                    print(food.f_calories)
                    food.serving_size = nutrientdict['serving_size_g']
                    food.fat = nutrientdict['fat_total_g']
                    food.protein = nutrientdict['protein_g']
                    food.carbs = nutrientdict['carbohydrates_total_g']
                    food.cholesterol = nutrientdict['cholesterol_mg']
                    print(request.user)
                    food.creator = request.user
                    food.save()
                # q1 = Food.objects.filter(creator=request.user)
                # q2 = q1.filter(created=timezone.now())
    else:
        form = CaloForm()

    today1 = date.today()
    today = date.strftime(today1, "%m-%d-%Y")
    history = {}
    total_calories = 0
    userdetails = {}
    user={}
    gender = 'male'
    user_age = 0
    weight = 45
    height = 130
    Goal = ''
    Fitness = ''
    context=''
    user_calo_comparison = {}
    eachday = Food.objects.filter(creator=username)
    # print(eachday)
    for i in eachday.values():
        print("keys:{}".format(i))

    for day in eachday.values():
        eday = day['created']
        category = day['category']
        currentday = date.strftime(eday, "%m-%d-%Y")
        today1 = date.today()
        today = date.strftime(today1, "%m-%d-%Y")

        if currentday == today:
            if today not in history:
                history[today] = {}

            if category not in history[today]:
                history[today][category] = []
            history[today][category].append(day)
            total_calories = total_calories + day['f_calories']
    print("history:",history)
    print("total_calories:",total_calories)

    userdetails = UserDetails.objects.filter(creator=request.user)
    userobjects = UserDetails.objects.filter(creator=request.user)
    for object in userobjects:
        user_age = object.age()
    for eachrow in userdetails.values():
        gender = eachrow['Gender']
        weight = eachrow['weight']
        weight_goal = eachrow['weight_goal']
        height = eachrow['height']
        Goal = eachrow['Goal']
        Fitness = eachrow['Fitness']
        print("userdata:",gender,weight,height,Goal,Fitness)
    user = {'age':user_age,'gender':gender,'weight':weight,'height':height}
    if Fitness == 'no_exercise':
        user['activitylevel'] = 'level_1'
    elif Fitness == 'mild_exercise':
        user['activitylevel'] ='level_3'
    else:
        user['activitylevel'] = 'level_4'

    # Ideal Daily Calorie Requirements
    DailyCalorieResponse = FitnessApi(user)
    print("dailycalo:",DailyCalorieResponse)
    for idealcalo in DailyCalorieResponse.values():
        # user_calo_comparison['BMR'] = idealcalo["data"]["BMR"]
        print(idealcalo)
        weight_goal1 = idealcalo["data"]["goals"]
        print("weight:",weight_goal1)
        for goals,values in weight_goal1.items():
            if Goal == "maintain_weight" and goals == 'maintain weight':
                user_calo_comparison[goals] == values
            elif Goal == "loose_weight" and goals == 'Weight loss':
                user_calo_comparison[goals] = values
            elif Goal == "gain_weight" and goals == 'Weight gain':
                user_calo_comparison[goals] = values
    print("compare:",user_calo_comparison)
    for idealreq, req in user_calo_comparison.items():
        if type(req) is dict:
            print(req['calory'])
            print(total_calories)
            context = maintain_calories(req['calory'],total_calories)
        elif idealreq == "maintain weight":
            context = maintain_calories(req, total_calories)


    print("level:",context)

    return render(request, "user/calo.html", {"form": form, "history": history,'user_calo_comparison':user_calo_comparison,'total_calories':total_calories,'context':context})

def maintain_calories(ideal_calo,total_calories):
    string1 = ""
    if decimal.Decimal(ideal_calo) == total_calories:
        string1 = "Perfect Level"
    elif ideal_calo > total_calories:
        addcalo = round((decimal.Decimal(ideal_calo) - total_calories),1)
        string1 = "Increase "+str(addcalo)+" for Perfect Level"
    elif ideal_calo < total_calories:
        subcalo =  round((total_calories - decimal.Decimal(ideal_calo)),1)

        string1 = "Reduce "+str(subcalo)+" for Perfect Level"
    else:
        string1 = "No Entries of Food Today"

    return string1
































   #
                # for date1, values in history.items():
                #     for category, food_items in values.items():
                #         for food in food_items:



                # # currentday = datetime.strptime(str(eday), '%Y-%m-%d').date()
                # # currentday = str(eday).strip()
                # # print(eday)
                # currentday = date.strftime(eday,"%m-%d-%Y")
                # today1 = date.today()
                # today = date.strftime(today1,"%m-%d-%Y")
                # if currentday == today:
                #     if currentday not in history:
                #         print('b')
                #         history[currentday] = []
                #         for cday, catelist in history.items():
                #             print(len(catelist))
                #             if len(catelist) == 0:
                #                 history[cday].append({day['category']: []})
                #                 for catedict in catelist:
                #                     for categry, itemlist in catedict.items():
                #                         if day['category'] == 'breakfast':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'lunch':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'dinner':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'snacks':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         else:
                #                             catedict[categry].append("No updates today")
                #     else:
                #         for cday, catelist in history.items():
                #             print(len(catelist))
                #             if len(catelist) == 0:
                #                 history[cday].append({day['category']: []})
                #                 for catedict in catelist:
                #                     for categry, itemlist in catedict.items():
                #                         if day['category'] == 'breakfast':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'lunch':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 print("ultranewuser:{}".format(dict1))
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'dinner':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         elif day['category'] == 'snacks':
                #                             if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                 dict1 = {}
                #                                 dict1['name'] = day['name']
                #                                 dict1['serving_size'] = day['serving_size']
                #                                 dict1['calories'] = day['f_calories']
                #                                 dict1['fat'] = day['fat']
                #                                 dict1['carbs'] = day['carbs']
                #                                 dict1['protein'] = day['protein']
                #                                 catedict[categry].append(dict1)
                #                         else:
                #                             catedict[categry].append("No updates today")
                #             else:
                #                 for catedict in catelist:
                #                     print(day['category'])
                #                     print(catelist)
                #                     if day['category'] not in catedict:
                #                         print('x')
                #                         print("category:{}".format(day['category']))
                #                         history[cday].append({day['category']: []})
                #                         for categry, itemlist in catedict.items():
                #                             if day['category'] == 'breakfast':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                             elif day['category'] == 'lunch':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                                     print("new_cate_everytime:{}".format(dict1))
                #                                     print("new_cate:{}".format(catedict))
                #                             elif day['category'] == 'dinner':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                             elif day['category'] == 'snacks':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                             else:
                #                                 catedict[categry].append("No updates today")
                #                     else:
                #                         for categry, itemlist in catedict.items():
                #                             if day['category'] == 'breakfast':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                             elif day['category'] == 'lunch':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                                     print("alreadyder:{}".format(dict1))
                #                             elif day['category'] == 'dinner':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                                     print("dinner:{}".format(catedict))
                #                             elif day['category'] == 'snacks':
                #                                 if day.keys() != 'created' or day.keys() != 'creator' or day.keys() != 'category':
                #                                     dict1 = {}
                #                                     dict1['name'] = day['name']
                #                                     dict1['serving_size'] = day['serving_size']
                #                                     dict1['calories'] = day['f_calories']
                #                                     dict1['fat'] = day['fat']
                #                                     dict1['carbs'] = day['carbs']
                #                                     dict1['protein'] = day['protein']
                #                                     catedict[categry].append(dict1)
                #                             else:
                #                                 catedict[categry].append("No updates today")
                #                 print(catedict.keys())

        

