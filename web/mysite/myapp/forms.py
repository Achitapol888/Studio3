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
    preferences = forms.MultipleChoiceField(
        choices=UserProfile.USER_PREFERENCES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'dorm', 'phone_number', 'student_ID', 'preferences', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@kkumail.com') or email.endswith('@kku.ac.th')):
                raise forms.ValidationError("Email must end with '@kkumail.com' or '@kku.ac.th'.")
        return email

    def clean_preferences(self):
        preferences = self.cleaned_data.get('preferences')
        if preferences and len(preferences) > 3:
            raise forms.ValidationError("You can select a maximum of 3 preferences.")
        return preferences

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  # Save first name
        user.last_name = self.cleaned_data['last_name']    # Save last name
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                dorm=self.cleaned_data['dorm'],
                phone_number=self.cleaned_data['phone_number'],
                student_ID=self.cleaned_data['student_ID'],
                preferences=self.cleaned_data['preferences'],
            )
        return user
