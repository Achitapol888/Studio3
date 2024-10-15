from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)  # Add first name field
    last_name = forms.CharField(max_length=30, required=True)   # Add last name field
    dorm = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    student_ID = forms.IntegerField(required=True)
    profile_picture = forms.ImageField(required=False)  # Correctly define this field here

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'dorm', 'phone_number', 'student_ID',
                  'password1', 'password2']  # Removed 'profile_picture' from User fields

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@kkumail.com') or email.endswith('@kku.ac.th')):
                raise forms.ValidationError("Email must end with '@kkumail.com' or '@kku.ac.th'.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  # Save first name
        user.last_name = self.cleaned_data['last_name']    # Save last name
        if commit:
            user.save()
            # Save profile data in UserProfile
            user_profile = UserProfile.objects.create(
                user=user,
                dorm=self.cleaned_data['dorm'],
                phone_number=self.cleaned_data['phone_number'],
                student_ID=self.cleaned_data['student_ID'],
                profile_picture=self.cleaned_data.get('profile_picture')  # Corrected profile_picture
            )
        return user


#Below are for edit profile pages
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dorm', 'phone_number', 'student_ID', 'profile_picture']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@kkumail.com') or email.endswith('@kku.ac.th')):
                raise forms.ValidationError("Email must end with '@kkumail.com' or '@kku.ac.th'.")
        return email