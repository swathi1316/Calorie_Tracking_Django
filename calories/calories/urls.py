"""calories URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from homepage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homeview, name="home"),
    path("register/", views.usersignup, name="register"),
    path("search/", views.SearchTemplateView, name="search"),
    path('registration/', include("django.contrib.auth.urls"),name='login'),
    path('user/', views.userdetailview,name='details'),
    path('calo/tracking/', views.UserTracking, name='tracking'),
    path('user_logout/',views.logout_view,name='logout'),
]
print(urlpatterns)
