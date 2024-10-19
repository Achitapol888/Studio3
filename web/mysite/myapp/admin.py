from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, PostGiver, PostReceiver

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'profile_picture_display',
        'dorm',
        'phone_number',
        'student_ID'
    )
    search_fields = ('user__username', 'dorm', 'student_ID')
    list_filter = ('dorm',)

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.profile_picture.url)
        return "No Picture"
    
    profile_picture_display.short_description = 'Profile Picture'

class PostGiverAdmin(admin.ModelAdmin):
    list_display = (
        'stuff_name',
        'categories',
        'user_profile',
        'stuff_picture_display',
        'description',   # Included
        'defect',        # Included
        'place',         # Included
        'date_limit',    # Included
        'created_at',
        'updated_at',
        'is_matched',    # Included
        'is_verify'      # Included
    )
    search_fields = ('stuff_name', 'user_profile__user__username')
    list_filter = ('categories', 'defect', 'created_at')

    def stuff_picture_display(self, obj):
        if obj.stuff_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.stuff_picture.url)
        return "No Picture"

    stuff_picture_display.short_description = 'Stuff Picture'

class PostReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'stuff_name',
        'categories',
        'user_profile',
        'description',   # Included
        'defect',        # Included
        'place',         # Included
        'date_limit',    # Included
        'created_at',
        'updated_at',
        'is_matched',    # Included
        'is_verify'      # Included
    )
    search_fields = ('stuff_name', 'user_profile__user__username')
    list_filter = ('categories', 'defect', 'created_at')


# Register the models with the admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PostGiver, PostGiverAdmin)
admin.site.register(PostReceiver, PostReceiverAdmin)
