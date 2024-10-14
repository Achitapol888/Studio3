from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User

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
            messages.success(request, "Registration successful! You can now log in.")
            print("User created:", user) 
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'myweb/register.html', {'form': form})

def select_prefer(request):
    return render(request, "myweb/select_prefer.html")

@login_required
def profile(request):
    user = request.user  # Get the currently logged-in user
    user_profile = user.profile
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'myweb/profile.html', context)

def role_selection(reqest):
    return render(reqest, "myweb/role_selection.html")

def receiver(reqest):
    return render(reqest, "myweb/receiver.html")

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