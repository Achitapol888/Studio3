from django.db import models
from django.contrib.auth.models import User
class Dorm(models.Model):
    dorm_ID = models.AutoField(primary_key=True)
    dorm_name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length = 30, blank=True, null=True)
    first_name = models.CharField(max_length = 30, blank=True, null=True)
    surname = models.CharField(max_length = 30, blank=True, null=True)
    nick_name = models.CharField(max_length = 30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    prefer_items = models.TextField(default='[]')  # Store as JSON or comma-separated values
    history = models.TextField(default='[]')  # Same as above
    student_ID = models.CharField(max_length=15, unique=True)
    kku_mail = models.EmailField(max_length=100, unique=True)
    dorm = models.ForeignKey(Dorm, on_delete=models.SET_NULL, null=True)

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('giver', 'Giver'),
        ('receiver', 'Receiver'),
    ]
    post_ID = models.AutoField(primary_key=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    item_type = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    photo_image = models.ImageField(upload_to='images/')
    detail = models.CharField(max_length=300)
    quantity = models.IntegerField()
    flaw = models.CharField(max_length=300)
    date_limit = models.DateTimeField()
    post_time = models.TimeField()
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # New field


class Chat(models.Model):
    chat_ID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Verify(models.Model):
    verify_ID = models.AutoField(primary_key=True)
    verify_status = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    verifier = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Review(models.Model):
    review_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.FloatField()
    content = models.TextField()
    verify = models.ForeignKey(Verify, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
