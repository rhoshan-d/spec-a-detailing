from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order
from .forms import OrderForm


class OrderFormTest(TestCase):
    """Tests for the Order form"""
    
    def test_order_form_valid_data(self):
        """Test the Order form with valid data"""
        form = OrderForm(data={
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test St',
            'town_or_city': 'Test City',
            'country': 'IE',
        })
        self.assertTrue(form.is_valid())
    
    def test_order_form_no_data(self):
        """Test the Order form with no data"""
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # 6 required fields


class CheckoutViewsTest(TestCase):
    """Tests for checkout views"""
    
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_checkout_view_empty_bag(self):
        """Test checkout view with empty bag redirects"""
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('products'))