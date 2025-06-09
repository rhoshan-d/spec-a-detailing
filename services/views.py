from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Service, Booking
from .forms import BookingForm


def all_services(request):
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})


def all_services(request):
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'services/service_detail.html', {'service': service})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, service=service)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()

            messages.success(
                request, f"Your booking for {service.name} on {booking.booking_date} has been received!")
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm(service=service)

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'services/book_service.html', context)


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'services/booking_confirmation.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user).order_by('booking_date')
    return render(request, 'services/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        if booking.can_cancel():
            booking.status = 'cancelled'
            booking.save()
            messages.success(
                request, f"Your booking for {booking.service.name} has been cancelled.")
        else:
            messages.error(
                request, "Bookings can only be cancelled at least 24 hours in advance.")
        return redirect('my_bookings')

    return render(request, 'services/cancel_booking.html', {'booking': booking})


def get_unavailable_dates(request, service_id):
    today = timezone.now().date()
    end_date = today + timedelta(days=60)

    date_slots = {}

    bookings = Booking.objects.filter(
        booking_date__gte=today,
        booking_date__lte=end_date,
        status__in=['pending', 'confirmed']
    )

    for booking in bookings:
        date_str = booking.booking_date.strftime('%Y-%m-%d')
        if date_str not in date_slots:
            date_slots[date_str] = set()
        date_slots[date_str].add(booking.time_slot)

    fully_booked_dates = []
    partially_booked = []

    for date, slots in date_slots.items():
        if 'morning' in slots and 'afternoon' in slots:
            fully_booked_dates.append(date)
        else:
            for slot in slots:
                partially_booked.append({'date': date, 'slot': slot})

    return JsonResponse({
        'fully_booked': fully_booked_dates,
        'partially_booked': partially_booked
    })
