from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('user', 'profile_picture_display', 'dorm', 'phone_number', 'student_ID')

    # Add search functionality on specific fields
    search_fields = ('user__username', 'dorm', 'student_ID')

    # Add filters based on dorm or other fields if necessary
    list_filter = ('dorm',)

    # Method to display the profile picture in the admin list view
    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.profile_picture.url)
        return "No Picture"

    profile_picture_display.short_description = 'Profile Picture'

# Register the UserProfile model with the admin site
admin.site.register(UserProfile, UserProfileAdmin)
