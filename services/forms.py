from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form for creating a new booking.
    This form allows users to select a booking date, time slot, address,
    and any special instructions they may have.
    """
    booking_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'text', 'class': 'form-control datepicker', 'readonly': 'readonly'}),
        help_text="Select your preferred date"
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'time_slot',
                  'address', 'special_instructions']
        widgets = {
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)
        self.fields['booking_date'].label = "Preferred Date"
        self.fields['time_slot'].label = "Preferred Time"
        self.fields['special_instructions'].label = "Special Instructions (Optional)"

    def clean_booking_date(self):
        """
        Validate the booking date to ensure it is not in the past,
        is at least one day in advance,
        and does not exceed 60 days in the future.
        """
        booking_date = self.cleaned_data['booking_date']
        today = timezone.now().date()

        if booking_date < today:
            raise forms.ValidationError("Booking date cannot be in the past.")

        if booking_date < today + timedelta(days=1):
            raise forms.ValidationError(
                "Bookings must be made at least 1 day in advance.")

        if booking_date > today + timedelta(days=60):
            raise forms.ValidationError(
                "Bookings cannot be made more than 60 days in advance.")

        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        time_slot = cleaned_data.get('time_slot')

        if booking_date and time_slot and self.service:
            existing_booking = Booking.objects.filter(
                service=self.service,
                booking_date=booking_date,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).exists()

            if existing_booking:
                raise forms.ValidationError(
                    f"This {time_slot} slot is already booked for {booking_date}. "
                    "Please select a different date or time slot."
                )

        return cleaned_data
