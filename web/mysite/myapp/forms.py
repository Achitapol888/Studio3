"""from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='ป้อนรหัสผ่านอีกครั้ง')

    class Meta:
        model = Profile
        fields = ['first_name', 'surname', 'phone_number', 'kku_mail', 'student_ID', 'dorm']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "รหัสผ่านไม่ตรงกัน")

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['kku_mail'],  # You can use email as username
            password=self.cleaned_data['password']
        )
        user_profile = super().save(commit=False)
        user_profile.user = user  # Link the UserProfile to the User instance

        if commit:
            user_profile.save()
        return user_profile

"""