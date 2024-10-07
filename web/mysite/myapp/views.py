from django.shortcuts import render
from django.shortcuts import HttpResponse

def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")

def base(request):
    return render(request, "myweb/base.html")

def role_selection(reqest):
    return render(reqest, "myweb/role_selection.html")

def home(request):
    return render(request, "myweb/home.html")

def login(request):
    return render(request, "myweb/login.html")

def register(request):
    return render(request, "myweb/register.html")

def select_prefer(request):
    return render(request, "myweb/select_prefer.html")
