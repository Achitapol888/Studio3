from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from .forms import SignUpForm, UserForm, UserProfileForm, PostGiverForm, PostReceiverForm
from .models import UserProfile, PostGiver, PostReceiver, MatchPost
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.urls import reverse
from fuzzywuzzy import fuzz
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
            return redirect('results_receiver', post_ID=post.post_ID)  # Pass the post_id here
    else:
        form = PostReceiverForm()
    return render(request, "myweb/receiver.html", {'form': form})

@login_required
def giver(request):
    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = request.user.profile
            post.save()
            # Redirect to the results_giver view with the new post_id
            return redirect('results_giver', post_ID=post.post_ID)  # Pass the post_id here
    else:
        form = PostGiverForm()

    return render(request, "myweb/giver.html", {'form': form})


@login_required
def post_history(request, profile_id):
    # Retrieve the user profile based on the provided profile_id
    user_profile = get_object_or_404(UserProfile, id=profile_id)

    # Query posts for the specified user profile
    giver_posts = PostGiver.objects.filter(user_profile=user_profile)
    receiver_posts = PostReceiver.objects.filter(user_profile=user_profile)

    # Retrieve matched posts where the user is either the giver or the receiver
    matched_posts = MatchPost.objects.filter(
        giver_post__user_profile=user_profile
    ).union(MatchPost.objects.filter(
        receiver_post__user_profile=user_profile
    ))

    # Print the match_IDs for debugging
    for matched in matched_posts:
        match_id = matched.match_ID
        print(match_id)
    context = {
        'user': request.user,
        'giver_posts': giver_posts,
        'receiver_posts': receiver_posts,
        'user_profile': user_profile,
        'matched_posts': matched_posts,
    }

    return render(request, "myweb/post_history.html", context)


# Edit Giver Post
@login_required
def edit_giver_post(request, post_ID):
    post = get_object_or_404(PostGiver, post_ID=post_ID)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = PostGiverForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_history', profile_id=user_profile.id) 
    else:
        form = PostGiverForm(instance=post)

    return render(request, 'myweb/edit_giver_post.html', {
        'form': form,
        'post': post,
        'user_profile': user_profile 
    })

# Edit Receiver Post
@login_required
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
@login_required
def delete_receiver_post(request, post_ID):
    post = get_object_or_404(PostReceiver, post_ID=post_ID)

    if request.method == 'POST':
        post.delete()
        # Use the related_name to access the user profile
        if hasattr(request.user, 'profile'):
            return redirect('post_history', profile_id=request.user.profile.id)  

    return render(request, 'myweb/delete_post_confirmation.html', {'post': post})


# Delete Giver Post
@login_required
def delete_giver_post(request, post_ID):
    post = get_object_or_404(PostGiver, post_ID=post_ID)

    if request.method == 'POST':
        post.delete()
        if hasattr(request.user, 'profile'):
            return redirect('post_history', profile_id=request.user.profile.id) 

    return render(request, 'myweb/delete_post_confirmation.html', {'post': post})

@login_required
def search_matches_receiver(request, post_ID):
    current_receiver_post = get_object_or_404(PostReceiver, post_ID=post_ID)
    current_user = request.user
    best_match = None 

    receiver_category = current_receiver_post.categories
    receiver_item_name = current_receiver_post.stuff_name
    receiver_date_limit = current_receiver_post.date_limit

    matching_givers = PostGiver.objects.filter(
        categories=receiver_category,
        date_limit__gte=timezone.now().date(),  
    ).exclude(user_profile__user=current_user).exclude(is_matched=True) 

    print(f"Number of matching givers: {matching_givers.count()}") 

    filtered_givers = []
    for giver in matching_givers:
        similarity = fuzz.token_set_ratio(receiver_item_name, giver.stuff_name)
        date_difference = (receiver_date_limit - giver.date_limit).days
                
        if similarity > 0:
            filtered_givers.append((giver, similarity, date_difference))

    if filtered_givers:
        filtered_givers.sort(key=lambda x: (-x[1], x[2]))
        best_match = filtered_givers[0][0]  

    context = {
        'matching_givers': matching_givers,
        'best_match': best_match,
        'filtered_receivers': filtered_givers,
        'current_receiver_post': current_receiver_post,
    }

    if best_match:
        request.session['best_match_id'] = best_match.post_ID

    print(current_receiver_post.post_ID)
    if best_match:  
        print(best_match.post_ID)
    
    return render(request, 'myweb/results_receiver.html', context)



@login_required
def search_matches_giver(request, post_ID):
    current_giver_post = get_object_or_404(PostGiver, post_ID=post_ID)
    current_user = request.user
    best_match = None 

    if current_giver_post:
        giver_category = current_giver_post.categories
        giver_item_name = current_giver_post.stuff_name
        giver_date_limit = current_giver_post.date_limit
        
        matching_receivers = PostReceiver.objects.filter(
            categories=giver_category,
            date_limit__gte=timezone.now().date(),  
        ).exclude(user_profile__user=current_user).exclude(is_matched=True)

        filtered_receivers = []  
        for receiver in matching_receivers:
            similarity = fuzz.token_set_ratio(giver_item_name, receiver.stuff_name)
            date_difference = (giver_date_limit - receiver.date_limit).days
            
            if similarity > 0:  
                filtered_receivers.append((receiver, similarity, date_difference)) 

        if filtered_receivers:
            filtered_receivers.sort(key=lambda x: (-x[1], x[2])) 
            best_match = filtered_receivers[0][0] 

    context = {
        'matching_givers': current_giver_post,  
        'best_match': best_match,  
        'filtered_receivers': filtered_receivers, 
        'current_giver_post': current_giver_post,  
    }
    
    if best_match:
        request.session['best_match_id'] = best_match.post_ID

    print(current_giver_post.post_ID)
    if best_match:  
        print(best_match.post_ID)

    return render(request, 'myweb/results_giver.html', context)

@login_required
def verify_match(request, giver_post_id, receiver_post_id):
    current_giver_post = get_object_or_404(PostGiver, post_ID=giver_post_id)
    current_receiver_post = get_object_or_404(PostReceiver, post_ID=receiver_post_id)

    current_giver_post.is_matched = True
    current_giver_post.save()

    current_receiver_post.is_matched = True
    current_receiver_post.save()

    matched_post = MatchPost.objects.create(
        giver_post=current_giver_post,
        receiver_post=current_receiver_post
    )
    matched_post.confirmation_date = timezone.now()  
    matched_post.save() 
    return render(request, "myweb/verify.html", {'matched_post': matched_post})

@login_required
def confirm_verification(request, match_ID):
    match_post = get_object_or_404(MatchPost, match_ID=match_ID)

    match_post.confirmation_date = timezone.now()  
    match_post.save()

    giver_post = match_post.giver_post
    receiver_post = match_post.receiver_post

    giver_post.is_verify = True
    giver_post.save()

    receiver_post.is_verify = True
    receiver_post.save()

    return redirect('post_history', profile_id=request.user.profile.id)