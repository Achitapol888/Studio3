
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='Anonymous')
    surname = models.CharField(max_length=30, default='Anonymous')
    phone_number = models.CharField(max_length=15, default='Anonymous')
    student_ID = models.CharField(max_length=15, unique=True, primary_key=True)
    kku_mail = models.EmailField(max_length=100, unique=True)
    dorm = models.CharField(max_length=30, default='Anonymous')

    def __str__(self):
        return f"{self.first_name} {self.surname}"
# Create your models here.
