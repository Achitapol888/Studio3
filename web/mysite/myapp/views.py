from django.shortcuts import render
from django.shortcuts import HttpResponse

def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")

def home(request):
    return render(request, "myweb/home.html")

def register(request):
    return render(request, "myweb/register.html")


