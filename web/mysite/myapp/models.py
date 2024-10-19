from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


CATEGORIES = [
    ("หนังสือ", "หนังสือ"),
    ("เครื่องครัว", "เครื่องครัว"),
    ("อุปกรณ์เสริมสวย", "อุปกรณ์เสริมสวย"),
    ("เครื่องใช้ไฟฟ้า", "เครื่องใช้ไฟฟ้า"),
    ("เฟอร์นิเจอร์", "เฟอร์นิเจอร์"),
    ("อุปกรณ์สำหรับสัตว์เลี้ยง", "อุปกรณ์สำหรับสัตว์เลี้ยง"),
    ("เสื้อผ้า", "เสื้อผ้า"),
]

DEFECT = [
    ("ไม่มี", "ไม่มี"),
    ("น้อย", "น้อย"),
    ("ปานกลาง", "ปานกลาง"),
    ("มาก", "มาก"),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    dorm = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    student_ID = models.IntegerField()

    def __str__(self):
        return self.user.username


class PostGiver(models.Model):
    post_ID = models.AutoField(primary_key=True)
    stuff_name = models.CharField(max_length=50)
    categories = models.CharField(max_length=50, choices=CATEGORIES)
    stuff_picture = models.ImageField(upload_to="stuff_picture/", blank=True, null=True)
    description = models.TextField()
    defect = models.CharField(max_length=50, choices=DEFECT)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    place = models.TextField()
    date_limit = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_matched = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stuff_name} by {self.user_profile.user.username}"


class PostReceiver(models.Model):
    post_ID = models.AutoField(primary_key=True)
    stuff_name = models.CharField(max_length=50)
    categories = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField()
    defect = models.CharField(max_length=50, choices=DEFECT)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    place = models.TextField()
    date_limit = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_matched = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stuff_name} by {self.user_profile.user.username}"


class MatchPost(models.Model):
    match_ID = models.AutoField(primary_key=True)
    giver_post = models.ForeignKey(PostGiver, on_delete=models.CASCADE)
    receiver_post = models.ForeignKey(PostReceiver, on_delete=models.CASCADE)
    match_date = models.DateTimeField(default=timezone.now)
    confirmation_date = models.DateTimeField(null=True, blank=True)  # To store the confirmation date

    def __str__(self):
        return f"Match ID: {self.match_ID} between {self.giver_post} and {self.receiver_post}"

