from django.test import TestCase
from django.urls import reverse


class HomeViewsTest(TestCase):
    """Tests for the home app views"""
    
    def test_index_view(self):
        """Test the index view loads properly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')