from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from .forms import SignUpForm, UserForm, UserProfileForm, PostGiverForm, PostReceiverForm
from .models import UserProfile, PostGiver, PostReceiver, MatchPost, CATEGORIES, DEFECT
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
def results_post(request):
    return render(request, "myweb/results_post.html")

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

    # Retrieve matched posts where the user is the giver
    matched_post_giver = MatchPost.objects.filter(giver_post__user_profile=user_profile)

    # Retrieve matched posts where the user is the receiver
    matched_post_receiver = MatchPost.objects.filter(receiver_post__user_profile=user_profile)

    # Print the match_IDs for debugging
    for matched in matched_post_giver:
        match_id = matched.match_ID
        print(f"Giver Match ID: {match_id}")

    for matched in matched_post_receiver:
        match_id = matched.match_ID
        print(f"Receiver Match ID: {match_id}")

    context = {
        'user': request.user,
        'giver_posts': giver_posts,
        'receiver_posts': receiver_posts,
        'user_profile': user_profile,
        'matched_post_giver': matched_post_giver,
        'matched_post_receiver': matched_post_receiver,
    }
    
    print(receiver_posts)
    print(giver_posts)
    
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
        print(filtered_givers)

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
        print(best_match)
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
    matched_post.match_date = timezone.now()  
    matched_post.save() 
    return render(request, "myweb/verify.html", {'matched_post': matched_post})

@login_required
def confirm_verification_giver(request, match_ID):
    match_post = get_object_or_404(MatchPost, match_ID=match_ID)

    match_post.confirmation_date = timezone.now()  
    match_post.is_giver_confirm = True
    match_post.save()

    giver_post = match_post.giver_post
    receiver_post = match_post.receiver_post

    giver_post.is_confirm = True
    giver_post.save()
    
    receiver_post.is_confirm = True
    receiver_post.save()
    
    print(giver_post)
    print(receiver_post)

    return redirect('post_history', profile_id=request.user.profile.id)

@login_required
def confirm_verification_receiver(request, match_ID):
    match_post = get_object_or_404(MatchPost, match_ID=match_ID)

    match_post.confirmation_date = timezone.now()  
    match_post.is_receiver_confirm = True
    match_post.save()

    receiver_post = match_post.receiver_post

    receiver_post.is_confirm = True
    receiver_post.save()
    
    print(receiver_post)

    return redirect('post_history', profile_id=request.user.profile.id)


def unmatch_post(request, post_id, post_type):
    if post_type == 'giver':
        post = get_object_or_404(PostGiver, post_ID=post_id)
        # Check for a match post associated with this giver post
        match_post = MatchPost.objects.filter(giver_post=post).first()
    elif post_type == 'receiver':
        post = get_object_or_404(PostReceiver, post_ID=post_id)
        # Check for a match post associated with this receiver post
        match_post = MatchPost.objects.filter(receiver_post=post).first()
    else:
        return redirect('post_history', profile_id=request.user.profile.id)  # Handle invalid post_type

    if request.method == 'POST':
        # Unmatch the current post
        post.is_matched = False
        post.save()

        # If there's a corresponding match post, unmatch the other post as well
        if match_post:
            # Unmatch the corresponding post
            if post_type == 'giver':
                match_post.receiver_post.is_matched = False
                match_post.receiver_post.save()
            else:
                match_post.giver_post.is_matched = False
                match_post.giver_post.save()

            # Delete the match post
            match_post.delete()

    return redirect('post_history', profile_id=request.user.profile.id)

def match_info_giver(request, match_id):
    # Retrieve the MatchPost object or return a 404 if it doesn't exist
    match = get_object_or_404(MatchPost, match_ID=match_id)
    
    # Pass the match object to the template for display
    context = {
        'match': match,
    }
    return render(request, 'myweb/match_info_giver.html', context)

def match_info_receiver(request, match_id):
    # Retrieve the MatchPost object or return a 404 if it doesn't exist
    match = get_object_or_404(MatchPost, match_ID=match_id)
    
    # Pass the match object to the template for display
    context = {
        'match': match,
    }
    return render(request, 'myweb/match_info_receiver.html', context)

def search_posts(request):
    
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
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    place = request.GET.get("place", "")
    defect = request.GET.get("defect", "")

    user_profile = request.user.profile

    # Exclude the current user's posts
    giver_posts = PostGiver.objects.exclude(user_profile=user_profile)
    receiver_posts = PostReceiver.objects.exclude(user_profile=user_profile)

    # Filter by query, category, place, and defect
    if query:
        giver_posts = giver_posts.filter(stuff_name__icontains=query)
        receiver_posts = receiver_posts.filter(stuff_name__icontains=query)
    if category:
        giver_posts = giver_posts.filter(categories=category)
        receiver_posts = receiver_posts.filter(categories=category)
    if place:
        giver_posts = giver_posts.filter(place__icontains=place)
        receiver_posts = receiver_posts.filter(place__icontains=place)
    if defect:
        giver_posts = giver_posts.filter(defect=defect)
        receiver_posts = receiver_posts.filter(defect=defect)

    context = {
        "query": query,
        "category": category,
        "place": place,
        "defect": defect,
        "giver_posts": giver_posts,
        "receiver_posts": receiver_posts,
        "user_profile": user_profile,
        "CATEGORIES": CATEGORIES,
        "DEFECT": DEFECT,
    }
    return render(request, "myweb/search_posts.html", context)


