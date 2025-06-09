from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category


class BagViewsTest(TestCase):
    """Tests for the shopping bag views"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )
        
        self.product = Product.objects.create(
            category=self.category,
            sku='tst123',
            name='Test Product',
            description='This is a test product',
            price=99.99,
            rating=4.8,
            image='test.jpg'
        )
    
    def test_view_bag(self):
        """Test the view_bag view"""
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingbag/bag.html')
    
    def test_add_to_bag(self):
        """Test adding an item to the bag"""
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]), 
            {'quantity': 1, 'redirect_url': '/'}
        )
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(str(self.product.id) in self.client.session.get('bag', {}))
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 1)