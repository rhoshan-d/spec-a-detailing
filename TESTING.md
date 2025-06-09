### For the Products App:

```python
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


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
```

### For the Bag App (Shopping Bag):

```python
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
        # Adding an item to the bag should create a session variable
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]), 
            {'quantity': 1, 'redirect_url': '/'}
        )
        self.assertEqual(response.status_code, 302)  # Redirects
        
        # Check if the item is in the session
        self.assertTrue(str(self.product.id) in self.client.session.get('bag', {}))
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 1)
```

### For the Home App:

```python
from django.test import TestCase
from django.urls import reverse


class HomeViewsTest(TestCase):
    """Tests for the home app views"""
    
    def test_index_view(self):
        """Test the index view loads properly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
```

### For the Checkout App:

```python
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
```

### For the Profile App:

```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileModelTest(TestCase):
    """Tests for the UserProfile model"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # UserProfile should be created automatically via signals
        self.profile = UserProfile.objects.get(user=self.user)
    
    def test_profile_creation(self):
        """Test profile is created for new user"""
        self.assertEqual(self.profile.user, self.user)


class ProfileViewsTest(TestCase):
    """Tests for profile views"""
    
    def setUp(self):
        # Create a test user and log them in
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
```

### For the Gift Card Feature (Products App):

```python
# Append this to products/tests.py
from django.utils import timezone
from .models import GiftCard


class GiftCardModelTest(TestCase):
    """Tests for the GiftCard model"""
    
    def setUp(self):
        # Create a test gift card
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
        # Current gift card should not be expired
        self.assertFalse(self.gift_card.is_expired())
        
        # Create an expired gift card
        expired_card = GiftCard.objects.create(
            code='EXPIRED',
            original_value=50.00,
            remaining_value=50.00,
            expiry_date=timezone.now() - timezone.timedelta(days=1),
            email='test@example.com',
            is_active=True
        )
        self.assertTrue(expired_card.is_expired())
```

## 2. Running Your Tests

To run your tests, you can use the Django test command:

```bash
python manage.py test
```

To run tests for a specific app:

```bash
python manage.py test products
```

## 3. Creating a TESTING.md File

For a comprehensive project submission, it's good practice to also include a separate TESTING.md file that describes your testing approach:

```markdown
# Spec-A Detailing - Testing

## Contents

- [Automated Testing](#automated-testing)
  - [Unit Tests](#unit-tests)
- [Manual Testing](#manual-testing)
  - [User Story Testing](#user-story-testing)
  - [Feature Testing](#feature-testing)
- [Validation](#validation)
  - [HTML](#html)
  - [CSS](#css)
  - [JavaScript](#javascript)
  - [Python](#python)
  - [Accessibility](#accessibility)
  - [Performance](#performance)
- [Bugs](#bugs)
  - [Fixed Bugs](#fixed-bugs)
  - [Unfixed Bugs](#unfixed-bugs)

## Automated Testing

### Unit Tests

The project includes automated tests for key functionality. These tests cover model behavior, view responses, and form validation.

#### Running the Tests

Tests can be run using the following command:

```bash
python manage.py test
```

#### Test Coverage

- **Products App**: Tests for Product and Category models, products listing view, and product detail view
- **Checkout App**: Tests for OrderForm validation and checkout view behavior
- **Profiles App**: Tests for UserProfile model creation and profile view access control
- **Shopping Bag App**: Tests for bag view and add to bag functionality
- **Home App**: Tests for home page rendering
- **Gift Card Feature**: Tests for gift card creation, validation, and expiration checks

## Manual Testing

### User Story Testing

Each user story has been manually tested to ensure the acceptance criteria are met:

| User Story | Test Performed | Result |
|------------|----------------|--------|
| As a first-time visitor, I want to navigate the website intuitively | Navigated through main menu, service categories, and footer links without prior instruction | Pass |
| As a returning customer, I want to access my profile information | Logged in and navigated to profile page to verify saved information is displayed | Pass |
| As a site admin, I want to add new service offerings | Logged in as admin, added a new product and verified it appears in the store | Pass |

(Continue with all user stories)

### Feature Testing

| Feature | Test Description | Expected Result | Actual Result | Pass/Fail |
|---------|------------------|-----------------|---------------|-----------|
| User Registration | Complete registration form with valid data | Account created and verification email sent | As expected | Pass |
| Product Filtering | Select category filter from dropdown | Only products from selected category displayed | As expected | Pass |
| Shopping Bag | Add product, update quantity, remove product | Bag updates correctly with proper totals | As expected | Pass |
| Checkout | Complete purchase with test card details | Order processed and confirmation displayed | As expected | Pass |
| Gift Card Code | Purchase gift voucher and check for code generation | Code displayed on order confirmation and in email | As expected | Pass |

(Continue with all features)

## Validation

### HTML

All pages were validated using the W3C Markup Validation Service:
- Home page: No errors
- Products page: No errors
- Product detail page: No errors
- Checkout page: No errors
- Profile page: No errors

### CSS

CSS files were validated using the W3C CSS Validation Service:
- base.css: No errors
- checkout.css: No errors

### JavaScript

JavaScript files were validated using JSHint:
- stripe_elements.js: No errors
- countryfield.js: No errors

### Python

Python code was validated using PEP8 compliance tools:
- All Python files comply with PEP8 standards
- Minor warnings addressed where possible

### Accessibility

The site was tested for accessibility using the WAVE WebAIM tool:
- All pages passed with no errors
- Color contrast meets WCAG AA standard

### Performance

Performance testing was conducted using Lighthouse:
- Mobile scores: Performance 85%, Accessibility 95%, Best Practices 92%, SEO 98%
- Desktop scores: Performance 92%, Accessibility 96%, Best Practices 92%, SEO 100%

## Bugs

### Fixed Bugs

1. **Issue**: Shopping bag quantity selector not updating totals correctly
   **Fix**: Added JavaScript event listener for change events on quantity inputs

2. **Issue**: Gift card codes not generating on checkout completion
   **Fix**: Added gift card generation logic to checkout_success view and fixed the reference to grand_total variable

3. **Issue**: Stripe payments failing for small amounts under €0.50
   **Fix**: Added minimum charge validation check before payment attempt

### Known Issues

The following issues have been identified and are scheduled for resolution in the next update:

1. **Booking Date Display**: Unavailable/fully booked dates are displayed one day ahead of the actual date (if you book the 19th, it will show the 20th as booked) (FIXED??)

2. **iPad Layout Issue**: On iPad and smaller devices, the 'My Bookings' page displays the footer incorrectly

3. **Mobile Navigation**: Navigation limitations on iPad and smaller devices where users cannot easily return to the home page from certain sections (e.g., from profiles page, the burger icon styling needs to be updated to match site design) (Maybe it's fine the way it is with some minor adjustments ?)