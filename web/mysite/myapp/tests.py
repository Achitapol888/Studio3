from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import PostReceiver, PostGiver, UserProfile  # Adjust based on your actual model imports
from django.utils import timezone

