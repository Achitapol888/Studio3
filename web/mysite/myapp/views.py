from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'myweb/login.html'

def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")

def base(request):
    return render(request, "myweb/base.html")

def home(request):
    return render(request, "myweb/home.html")

def login(request):
    return render(request, "myweb/login.html")

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)  # Debugging line
            return redirect('login')
        else:
            print(form.errors)  # Check if form validation errors are happening
    else:
        form = SignUpForm()
    return render(request, 'myweb/register.html', {'form': form})

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