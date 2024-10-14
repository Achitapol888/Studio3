from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
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
        fields = ['username', 'email', 'dorm', 'phone_number', 'student_ID', 'preferences', 'password1', 'password2']

    def clean_preferences(self):
        preferences = self.cleaned_data.get('preferences')
        if preferences and len(preferences) > 3:
            raise forms.ValidationError("You can select a maximum of 3 preferences.")
        return preferences

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
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
