from django.shortcuts import render
from .models import UserProfile
from .matching import find_matches  # Import the matching function
from django.shortcuts import HttpResponse

def match_view(request):
    # Get the current user's profile
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Find matching posts using the matching function
    matches = find_matches(user_profile)
    
    # Render the matches in a template
    return render(request, 'matching_results.html', {'matches': matches})

def placeholder_view(request):
    return HttpResponse("This is a placeholder for the home page.")
