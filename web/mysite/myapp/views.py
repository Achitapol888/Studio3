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


class CustomLoginView(LoginView):
    template_name = 'myweb/login.html'

    def get_success_url(self):
        # Check if the user has a profile
        if hasattr(self.request.user, 'profile'):
            return reverse('profile', args=[self.request.user.profile.id])
        else:
            return reverse('login') 

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
    return render(request, 'myweb/edit.html', context)


@login_required
def receiver(request):
    if request.method == 'POST':
        form = PostReceiverForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            return redirect('results_receiver')
    else:
        form = PostReceiverForm()
    return render(request, "myweb/receiver.html", {'form': form})

@login_required
def giver(request):
    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the PostGiver data
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            # Redirect to the results_giver view with the new post_id
            return redirect('results_giver', post_id=post.post_ID)  # Pass the post_id here
    else:
        form = PostGiverForm()

    return render(request, "myweb/giver.html", {'form': form})


def post_history(request, profile_id):
    # Retrieve the user profile based on the provided profile_id
    user_profile = get_object_or_404(UserProfile, id=profile_id)

    # Query posts for the specified user profile
    giver_posts = PostGiver.objects.filter(user_profile=user_profile)
    receiver_posts = PostReceiver.objects.filter(user_profile=user_profile)

    context = {
        'giver_posts': giver_posts,
        'receiver_posts': receiver_posts,
        'user_profile': user_profile,
    }

    return render(request, "myweb/post_history.html", context)



# Edit Giver Post
def edit_giver_post(request, post_ID):
    post = get_object_or_404(PostGiver, post_ID=post_ID)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Redirect to the user's post history
            return redirect('post_history', profile_id=user_profile.id) 
    else:
        form = PostGiverForm(instance=post)

    # Pass user_profile into the template for URL usage
    return render(request, 'myweb/edit_giver_post.html', {
        'form': form,
        'post': post,
        'user_profile': user_profile  # Make sure user_profile is available in the template
    })

# Edit Receiver Post
def edit_receiver_post(request, post_ID):
    post = get_object_or_404(PostReceiver, post_ID=post_ID)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = PostReceiverForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Redirect to the user's post history
            return redirect('post_history', profile_id=user_profile.id) 
    else:
        form = PostReceiverForm(instance=post)

    # Pass user_profile into the template for URL usage
    return render(request, 'myweb/edit_receiver_post.html', {
        'form': form,
        'post': post,
        'user_profile': user_profile  # Make sure user_profile is available in the template
    })

# Delete Receiver Post
def delete_receiver_post(request, post_ID):
    post = get_object_or_404(PostReceiver, post_ID=post_ID)

    if request.method == 'POST':
        post.delete()
        # Use the related_name to access the user profile
        if hasattr(request.user, 'profile'):
            return redirect('post_history', profile_id=request.user.profile.id)  

    return render(request, 'myweb/delete_post_confirmation.html', {'post': post})


# Delete Giver Post
def delete_giver_post(request, post_ID):
    post = get_object_or_404(PostGiver, post_ID=post_ID)

    if request.method == 'POST':
        post.delete()
        # Use the related_name to access the user profile
        if hasattr(request.user, 'profile'):
            return redirect('post_history', profile_id=request.user.profile.id) 

    return render(request, 'myweb/delete_post_confirmation.html', {'post': post})

@login_required
def search_matches_receiver(request):
     # Fetch the latest PostReceiver entry
    try:
        latest_receiver_post = PostReceiver.objects.latest('created_at')  # Or 'post_ID'
    except PostReceiver.DoesNotExist:
        latest_receiver_post = None

    matching_givers = PostGiver.objects.none()  # Initialize empty queryset
    matching_receivers = None  # Initialize receiver as None

    if latest_receiver_post:
        # Get the category of the latest receiver post
        receiver_category = latest_receiver_post.categories
        
        # Search for matching givers based on the category
        matching_givers = PostGiver.objects.filter(categories=receiver_category)

        # Optionally, you can pass the latest receiver post as well
        matching_receivers = latest_receiver_post
    
    context = {
        'matching_givers': matching_givers,
        'matching_receivers': matching_receivers
    }
    print(context)

    return render(request, 'myweb/results_receiver.html', context)



@login_required
def search_matches_giver(request, post_id):
    # Fetch the PostGiver entry using the provided post_id
    current_giver_post = get_object_or_404(PostGiver, post_ID=post_id)

    # Get the current user
    current_user = request.user
    best_match = None  # Initialize best_match

    similarity_threshold = 70  # Set the similarity threshold

    if current_giver_post:
        # Get the category, item name, and date limit of the current giver post
        giver_category = current_giver_post.categories
        giver_item_name = current_giver_post.stuff_name
        giver_date_limit = current_giver_post.date_limit

        # Search for matching receivers based on category and valid date,
        # and exclude the current user's posts
        matching_receivers = PostReceiver.objects.filter(
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
        'matching_givers': current_giver_post,  # This will hold the current giver post
        'best_match': best_match,  # This will hold the best matching receiver
    }
    print(context)

    return render(request, 'myweb/results_giver.html', context)  # Update the template name as needed

def review(request):
    return render(request, "myweb/review.html")



def verify(request):
    return render(request, "myweb/verify.html")
