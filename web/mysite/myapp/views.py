from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
#from .forms import UserProfile



def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")

def base(request):
    return render(request, "myweb/base.html")

def home(request):
    return render(request, "myweb/home.html")

def login(request):
    return render(request, "myweb/login.html")


"""def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        student_ID = request.POST['student_ID']
        dorm = request.POST['dorm']
        kku_mail = request.POST['kku_mail']
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        user = User.objects.create_user(username=kku_mail, email=kku_mail, password=password)
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            surname=surname,
            student_ID=student_ID,
            dorm=dorm,
            phone_number=phone_number
        )

        return redirect('success')  # Redirect to a success page
    return render(request, 'myweb/register.html')"""


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