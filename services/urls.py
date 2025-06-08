from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_services, name='services'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('unavailable-dates/<service_id>/', views.get_unavailable_dates, name='get_unavailable_dates'),
]