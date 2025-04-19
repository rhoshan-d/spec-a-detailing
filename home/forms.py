from django import forms
from .models import CustomerReview

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['rating', 'name', 'location', 'review_text']
        
    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set custom placeholders, CSS classes, 
        and hide labels for the form fields.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'rating': 'Rating (1-5)',
            'name': 'Your Name',
            'location': 'Your Town (e.g., Celbridge)',
            'review_text': 'Your Thoughts',
        }
        
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False