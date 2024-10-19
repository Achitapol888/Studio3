from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from .forms import SignUpForm, UserForm, UserProfileForm, PostGiverForm, PostReceiverForm
from .models import UserProfile, PostGiver, PostReceiver
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.urls import reverse
from fuzzywuzzy import fuzz
from django.db.models import Q
from django.utils import timezone


CATEGORIES = [
    ("หนังสือ", "หนังสือ"),
    ("เครื่องครัว", "เครื่องครัว"),
    ("อุปกรณ์เสริมสวย", "อุปกรณ์เสริมสวย"),
    ("เครื่องใช้ไฟฟ้า", "เครื่องใช้ไฟฟ้า"),
    ("เฟอร์นิเจอร์", "เฟอร์นิเจอร์"),
    ("อุปกรณ์สำหรับสัตว์เลี้ยง", "อุปกรณ์สำหรับสัตว์เลี้ยง"),
    ("เสื้อผ้า", "เสื้อผ้า"),
]

DEFECT = [
    ("ไม่มี", "ไม่มี"),
    ("น้อย", "น้อย"),
    ("ปานกลาง", "ปานกลาง"),
    ("มาก", "มาก"),
]

class CustomLoginView(LoginView):
    template_name = 'myweb/login.html'

    def get_success_url(self):
        # Check if the user has a profile
        if hasattr(self.request.user, 'profile'):
            return reverse('profile', args=[self.request.user.profile.id])
        else:
            return reverse('login') 

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
def profile(request, id):
    user_profile = get_object_or_404(UserProfile, id=id)
    context = {
        'user': request.user,
        'user_profile': user_profile,
    }
    print(context)
    return render(request, 'myweb/profile.html', context)

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', id=user_profile.id)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }


#Create receiver post
@login_required
def receiver(request):
    if request.method == 'POST':
        form = PostReceiverForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            return redirect('result_receiver', post_id=post.post_ID)  # Fixed redirect
    else:
        form = PostReceiverForm()
    return render(request, "myweb/receiver.html", {'form': form})

#Create giver post
@login_required
def giver(request):
    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the PostGiver data
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            return redirect('results_giver', post_id=post.post_ID)
    else:
        form = PostGiverForm()

    return render(request, "myweb/giver.html", {'form': form})



def post_history(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)

    giver_posts = PostGiver.objects.filter(user_profile=user_profile)
    receiver_posts = PostReceiver.objects.filter(user_profile=user_profile)

    print(giver_posts)  # Debugging line
    context = {
        'giver_posts': giver_posts,
        'receiver_posts': receiver_posts,
        'user_profile': user_profile,
    }

    return render(request, 'myweb/post_history.html', context)


def edit_giver_post(request, post_id):
    post = get_object_or_404(PostGiver, id=post_id)
    if request.method == "POST":
        form = PostGiverForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostGiverForm(instance=post)
    return render(request, 'myweb/edit_giver_post.html', {'form': form})

def delete_giver_post(request, post_id):
    post = get_object_or_404(PostGiver, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    
def edit_receiver_post(request, post_id):
    post = get_object_or_404(PostReceiver, id=post_id)
    if request.method == "POST":
        form = PostReceiverForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = PostReceiverForm(instance=post)
    return render(request, 'myweb/edit_giver_post.html', {'form': form})

def delete_receiver_post(request, post_id):
    post = get_object_or_404(PostReceiver, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('home')


def review(request):
    return render(request, "myweb/review.html")

def verify(request):
    return render(request, "myweb/verify.html")

@login_required
def search_matches_receiver(request, post_id):
   # Fetch the PostGiver entry using the provided post_id
    current_receiver_post = get_object_or_404(PostReceiver, post_ID=post_id)

    # Get the current user
    current_user = request.user
    best_match = None  # Initialize best_match

    similarity_threshold = 70  # Set the similarity threshold

    if current_receiver_post:
        # Get the category, item name, and date limit of the current giver post
        giver_category = current_receiver_post.categories
        giver_item_name = current_receiver_post.stuff_name
        giver_date_limit = current_receiver_post.date_limit

        # Search for matching receivers based on category and valid date,
        # and exclude the current user's posts
        matching_receivers = PostGiver.objects.filter(
            categories=giver_category,
            date_limit__gte=timezone.now().date(),  # Ensure the date limit is in the future
        ).exclude(user_profile__user=current_user)  # Exclude the current user

        # Filter matching receivers based on item name similarity
        filtered_receivers = []
        for receiver in matching_receivers:
            similarity = fuzz.token_set_ratio(giver_item_name, receiver.stuff_name)
            if similarity >= similarity_threshold:
                # Calculate the difference in days between giver and receiver date limits
                date_difference = (receiver.date_limit - giver_date_limit).days
                # Only consider future dates
                if date_difference >= 0:
                    filtered_receivers.append((receiver, similarity, date_difference))  # Store receiver with its similarity score and date difference

        # Select the receiver with the highest similarity score and the smallest date difference
        if filtered_receivers:
            # Sort by similarity score first, then by date difference
            filtered_receivers.sort(key=lambda x: (-x[1], x[2]))  # Sort by similarity descending, then by date difference ascending
            best_match = filtered_receivers[0][0]  # Get the receiver with the best score

    context = {
        'matching_receiver': current_receiver_post,  # This will hold the current giver post
        'best_match': best_match,  # This will hold the best matching receiver
    }
    print(context)

    return render(request, 'myweb/results_giver.html', context)  # Update the template name as needed



@login_required
def search_matches_giver(request, post_id):
    current_giver_post = get_object_or_404(PostGiver, post_ID=post_id)

    current_user = request.user
    best_match = None  

    similarity_threshold = 70  

    if current_giver_post:
        giver_category = current_giver_post.categories
        giver_item_name = current_giver_post.stuff_name
        giver_date_limit = current_giver_post.date_limit

        matching_receivers = PostReceiver.objects.filter(
            categories=giver_category,
            date_limit__gte=timezone.now().date(),  
        ).exclude(user_profile__user=current_user)  

        filtered_receivers = []
        for receiver in matching_receivers:
            similarity = fuzz.token_set_ratio(giver_item_name, receiver.stuff_name)
            if similarity >= similarity_threshold:
                # Calculate the difference in days between giver and receiver date limits
                date_difference = (receiver.date_limit - giver_date_limit).days
                # Only consider future dates
                if date_difference >= 0:
                    filtered_receivers.append((receiver, similarity, date_difference))  # Store receiver with its similarity score and date difference

        # Select the receiver with the highest similarity score and the smallest date difference
        if filtered_receivers:
            # Sort by similarity score first, then by date difference
            filtered_receivers.sort(key=lambda x: (-x[1], x[2]))  # Sort by similarity descending, then by date difference ascending
            best_match = filtered_receivers[0][0]  # Get the receiver with the best score

    context = {
        'matching_givers': current_giver_post,  # This will hold the current giver post
        'best_match': best_match,  # This will hold the best matching receiver
    }
    print(context)

    return render(request, 'myweb/results_giver.html', context)  # Update the template name as needed





