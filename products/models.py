from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_gift_voucher = models.BooleanField(default=False)
    validity_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="Validity period in months (for gift cards only)"
    )

    def __str__(self):
        return self.name


class GiftCard(models.Model):
    code = models.CharField(max_length=10, unique=True)
    original_value = models.DecimalField(max_digits=6, decimal_places=2)
    remaining_value = models.DecimalField(max_digits=6, decimal_places=2)
    expiry_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        'checkout.Order', null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Gift Card {self.code} - €{self.remaining_value}"

    def is_expired(self):
        return timezone.now() > self.expiry_date
