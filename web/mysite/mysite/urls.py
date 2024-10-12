"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path('base/', views.base, name = 'base'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('select-prefer/', views.select_prefer, name="select-prefer"), 
    path('role-selection/', views.role_selection, name='role-selection'),
    path('reciver/', views.reciver, name='reciver'),
    path('giver/', views.giver, name='giver'),
    path('profile/', views.profile, name= 'profile'),
    path('review/', views.review, name= 'review'),
    path('result_for_receiver/', views.result_for_receiver, name= 'result_for_receiver'),
    path('result_for_giver/', views.result_for_giver, name= 'result_for_giver'),
    path('verify/', views.verify, name= 'verify'),
]
