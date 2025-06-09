from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileModelTest(TestCase):
    """Tests for the UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_creation(self):
        """Test profile is created for new user"""
        self.assertEqual(self.profile.user, self.user)


class ProfileViewsTest(TestCase):
    """Tests for profile views"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view(self):
        """Test the profile page loads when logged in"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_view_not_logged_in(self):
        """Test profile redirects if not logged in"""
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response,
                             '/accounts/login/?next=/profile/')
