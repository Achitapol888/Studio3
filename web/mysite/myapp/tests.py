from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, PostGiver, PostReceiver, MatchPost

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            dorm='Dorm A',
            phone_number=1234567890,
            student_ID=12345678
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.dorm, 'Dorm A')
        self.assertEqual(self.user_profile.phone_number, 1234567890)
        self.assertEqual(self.user_profile.student_ID, 12345678)

class PostGiverTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            dorm='Dorm A',
            phone_number=1234567890,
            student_ID=12345678
        )
        self.post_giver = PostGiver.objects.create(
            stuff_name='Laptop',
            categories='Electronics',
            description='Used laptop in good condition',
            defect='None',
            user_profile=self.user_profile,
            place='Dorm A',
            date_limit='2024-12-31'
        )

    def test_post_giver_creation(self):
        self.assertEqual(self.post_giver.stuff_name, 'Laptop')
        self.assertEqual(self.post_giver.user_profile.user.username, 'testuser')
        self.assertFalse(self.post_giver.is_matched)

class PostReceiverTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            dorm='Dorm A',
            phone_number=1234567890,
            student_ID=12345678
        )
        self.post_receiver = PostReceiver.objects.create(
            stuff_name='Phone',
            categories='Electronics',
            description='Looking for a used phone',
            defect='None',
            user_profile=self.user_profile,
            place='Dorm A',
            date_limit='2024-12-31'
        )

    def test_post_receiver_creation(self):
        self.assertEqual(self.post_receiver.stuff_name, 'Phone')
        self.assertEqual(self.post_receiver.user_profile.user.username, 'testuser')
        self.assertFalse(self.post_receiver.is_matched)

class MatchPostTest(TestCase):
    def setUp(self):
        self.user_giver = User.objects.create_user(username='giver', password='pass')
        self.user_receiver = User.objects.create_user(username='receiver', password='pass')
        self.user_profile_giver = UserProfile.objects.create(
            user=self.user_giver,
            dorm='Dorm A',
            phone_number=1234567890,
            student_ID=12345678
        )
        self.user_profile_receiver = UserProfile.objects.create(
            user=self.user_receiver,
            dorm='Dorm B',
            phone_number=1234567891,
            student_ID=87654321
        )
        self.post_giver = PostGiver.objects.create(
            stuff_name='Laptop',
            categories='Electronics',
            description='Used laptop',
            defect='None',
            user_profile=self.user_profile_giver,
            place='Dorm A',
            date_limit='2024-12-31'
        )
        self.post_receiver = PostReceiver.objects.create(
            stuff_name='Phone',
            categories='Electronics',
            description='Looking for a used phone',
            defect='None',
            user_profile=self.user_profile_receiver,
            place='Dorm B',
            date_limit='2024-12-31'
        )
        self.match_post = MatchPost.objects.create(
            giver_post=self.post_giver,
            receiver_post=self.post_receiver
        )

    def test_match_post_creation(self):
        self.assertEqual(self.match_post.giver_post.stuff_name, 'Laptop')
        self.assertEqual(self.match_post.receiver_post.stuff_name, 'Phone')
        self.assertIsNotNone(self.match_post.match_date)

