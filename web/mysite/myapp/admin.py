from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('user', 'dorm', 'phone_number', 'student_ID')

    # Add search functionality on specific fields
    search_fields = ('user__username', 'dorm', 'student_ID')

    # Add filters based on dorm or other fields if necessary
    list_filter = ('dorm',)

    def get_queryset(self, request):
        return super().get_queryset(request)

# Register the UserProfile model with the admin site
admin.site.register(UserProfile, UserProfileAdmin)
