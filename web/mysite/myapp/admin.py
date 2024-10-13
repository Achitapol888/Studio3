from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'kku_mail', 'phone_number', 'dorm', 'student_ID')
    search_fields = ('kku_mail', 'first_name', 'surname')

    def get_queryset(self, request):
        return super().get_queryset(request)

admin.site.register(UserProfile, UserProfileAdmin)

