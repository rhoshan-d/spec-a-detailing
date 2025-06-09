from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, GiftCard


class CategoryModelTest(TestCase):
    """Tests for the Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )
    
    def test_category_string_method(self):
        """Test the string representation of a category"""
        self.assertEqual(str(self.category), 'test_category')
    
    def test_get_friendly_name(self):
        """Test the get_friendly_name method"""
        self.assertEqual(self.category.get_friendly_name(), 'Test Category')


class ProductModelTest(TestCase):
    """Tests for the Product model"""
    
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
    
    def test_product_string_method(self):
        """Test the string representation of a product"""
        self.assertEqual(str(self.product), 'Test Product')


class ProductViewsTest(TestCase):
    """Tests for the products views"""
    
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
    
    def test_all_products_view(self):
        """Test the all products view"""
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertTrue('products' in response.context)
    
    def test_product_detail_view(self):
        """Test the product detail view"""
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.context['product'], self.product)


class GiftCardModelTest(TestCase):
    """Tests for the GiftCard model"""
    
    def setUp(self):
        self.gift_card = GiftCard.objects.create(
            code='TEST123',
            original_value=50.00,
            remaining_value=50.00,
            expiry_date=timezone.now() + timezone.timedelta(days=365),
            email='test@example.com',
            is_active=True
        )
    
    def test_gift_card_string_method(self):
        """Test the string representation of a gift card"""
        self.assertEqual(str(self.gift_card), f"Gift Card {self.gift_card.code} - €50.0")
    
    def test_gift_card_is_expired(self):
        """Test the is_expired method works correctly"""
        self.assertFalse(self.gift_card.is_expired())
        
        expired_card = GiftCard.objects.create(
            code='EXPIRED',
            original_value=50.00,
            remaining_value=50.00,
            expiry_date=timezone.now() - timezone.timedelta(days=1),
            email='test@example.com',
            is_active=True
        )
        self.assertTrue(expired_card.is_expired())