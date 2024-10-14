from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_PREFERENCES = [
        ('เครื่องใช้ไฟฟ้า', 'เครื่องใช้ไฟฟ้า (Electronics)'),
        ('เสื้อผ้า', 'เสื้อผ้า (Clothing)'),
        ('อุปกรณ์เสริมสวย', 'อุปกรณ์เสริมสวย (Beauty accessories)'),
        ('หนังสือ', 'หนังสือ (Books)'),
        ('เครื่องครัว', 'เครื่องครัว (Kitchenware)'),
        ('อุปกรณ์สำหรับสัตว์เลี้ยง', 'อุปกรณ์สำหรับสัตว์เลี้ยง (Pet care supplies)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dorm = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    student_ID = models.IntegerField()
    preferences = models.JSONField(null=True, default=list) 

    def __str__(self):
        return self.user.username


"""
class Post(models.Model):
    POST_TYPE_CHOICES = [('giver', 'Giver'), ('receiver', 'Receiver')]
    post_ID = models.AutoField(primary_key=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    item_type = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    photo_image = models.ImageField(upload_to='images/')
    detail = models.TextField()  # Using TextField for longer details
    quantity = models.IntegerField()
    flaw = models.TextField()  # Changed to TextField for flexibility
    date_limit = models.DateTimeField()
    post_time = models.DateTimeField(auto_now_add=True)  # Using DateTime for timestamp
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


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
"""
