from django.contrib import admin
from .models import Service, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'booking_date', 'time_slot', 'status', 'created_on')
    list_filter = ('status', 'booking_date', 'time_slot', 'service')
    search_fields = ('user__username', 'user__email', 'address', 'special_instructions')
    readonly_fields = ('created_on', 'updated_on')
    list_editable = ('status',)
    date_hierarchy = 'booking_date'