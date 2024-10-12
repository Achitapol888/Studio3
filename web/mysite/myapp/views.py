from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")

def base(request):
    return render(request, "myweb/base.html")

def home(request):
    return render(request, "myweb/home.html")

def login(request):
    return render(request, "myweb/login.html")

def register(request):
    return render(request, "myweb/register.html")

def select_prefer(request):
    return render(request, "myweb/select_prefer.html")

def profile(request):
    return render(request, "myweb/profile.html")

def role_selection(reqest):
    return render(reqest, "myweb/role_selection.html")

def reciver(reqest):
    return render(reqest, "myweb/reciver.html")

def giver(reqest):
    return render(reqest, "myweb/giver.html")

def review(request):
    return render(request, "myweb/review.html")

def result_for_receiver(request):
    return render(request, "myweb/result_for_receiver.html")

def result_for_giver(request):
    return render(request, "myweb/result_for_giver.html")

def verify(request):
    return render(request, "myweb/verify.html")