from .models import Post, UserProfile
from django.db.models import Q

def find_matches(user_profile):
    # Retrieve user preferences and dorm
    user_preferences = user_profile.prefer_items
    user_dorm = user_profile.dorm
    
    # Fetch all available posts (consider only the posts that are of type 'giver')
    available_posts = Post.objects.filter(post_type='giver')
    
    # Filter posts based on user preferences (matching item types)
    matched_posts = available_posts.filter(
        Q(item_type__in=user_preferences) | 
        Q(dorm=user_dorm)  # Optionally match by dorm
    )
    
    # Return a list of matching posts
    return matched_posts
