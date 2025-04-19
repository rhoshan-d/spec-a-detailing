from django.contrib import admin
from .models import CustomerReview

# Register your models here.

class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'location', 'created_date', 'approved')
    list_filter = ('approved', 'rating', 'created_date')
    search_fields = ('name', 'review_text', 'location')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
    approve_reviews.short_description = "Approve selected reviews"

admin.site.register(CustomerReview, CustomerReviewAdmin)