from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from .models import UserProfile, PostGiver, PostReceiver

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    dorm = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    student_ID = forms.IntegerField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'dorm', 'phone_number', 'student_ID',
                  'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'dorm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dorm'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'student_ID': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@kkumail.com') or email.endswith('@kku.ac.th')):
                raise forms.ValidationError("Email must end with '@kkumail.com' or '@kku.ac.th'.")

            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_student_ID(self):
        student_ID = self.cleaned_data.get('student_ID')
        if student_ID:
            # Check if the student ID is unique in UserProfile model
            if UserProfile.objects.filter(student_ID=student_ID).exists():
                raise forms.ValidationError("This student ID is already in use.")
        return student_ID
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                dorm=self.cleaned_data['dorm'],
                phone_number=self.cleaned_data['phone_number'],
                student_ID=self.cleaned_data['student_ID'],
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user



#edit profile forms
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dorm', 'phone_number', 'student_ID', 'profile_picture']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@kkumail.com') or email.endswith('@kku.ac.th')):
                raise forms.ValidationError("Email must end with '@kkumail.com' or '@kku.ac.th'.")

            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_student_ID(self):
        student_ID = self.cleaned_data.get('student_ID')
        if student_ID:
            # Check if the student ID is unique in UserProfile model
            if UserProfile.objects.filter(student_ID=student_ID).exists():
                raise forms.ValidationError("This student ID is already in use.")
        return student_ID
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    
# Post Giver Form
class PostGiverForm(forms.ModelForm):
    class Meta:
        model = PostGiver
        fields = ['stuff_name', 'categories', 'stuff_picture', 'description', 'defect', 'place', 'date_limit']
        widgets = {
            'stuff_name': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'stuff_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'defect': forms.Select(attrs={'class': 'form-control'}),
            'place': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'date_limit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_date_limit(self):
        date_limit = self.cleaned_data.get('date_limit')
        if date_limit and date_limit <= datetime.date.today():
            raise forms.ValidationError("The date must be in the future.")
        return date_limit

class PostReceiverForm(forms.ModelForm):
    class Meta:
        model = PostReceiver
        fields = ['stuff_name', 'categories', 'description', 'defect', 'place', 'date_limit']
        widgets = {
            'stuff_name': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'defect': forms.Select(attrs={'class': 'form-control'}),
            'place': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'date_limit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_date_limit(self):
        date_limit = self.cleaned_data.get('date_limit')
        if date_limit and date_limit <= datetime.date.today():
            raise forms.ValidationError("The date must be in the future.")
        return date_limit
