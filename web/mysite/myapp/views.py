from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, UserForm, UserProfileForm, PostGiverForm, PostReceiverForm
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
        form = SignUpForm(request.POST, request.FILES)
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

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        # Check if the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the forms
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to the profile page after success
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'myweb/edit.html', context)



def role_selection(request):
    return render(request, "myweb/role_selection.html")

@login_required
def receiver(request):
    if request.method == 'POST':
        form = PostReceiverForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            return redirect('profile')
    else:
        form = PostReceiverForm()
    return render(request, "myweb/receiver.html", {'form': form})

@login_required
def giver(request):
    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Create an instance but don't save it yet
            post.user_profile = request.user.profile  # Associate the current user's profile
            post.save()  # Now save the instance
            return redirect('profile')
    else:
        form = PostGiverForm()
    
    return render(request, "myweb/giver.html", {'form': form})

def review(request):
    return render(request, "myweb/review.html")

def result_for_receiver(request):
    return render(request, "myweb/result_for_receiver.html")

def result_for_giver(request):
    return render(request, "myweb/result_for_giver.html")

def verify(request):
    return render(request, "myweb/verify.html")