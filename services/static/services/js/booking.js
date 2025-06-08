document.addEventListener('DOMContentLoaded', function() {
    let unavailableDates = [];
    let partiallyBookedSlots = {};
    let selectedDate = null;

    const bookingDateInput = document.getElementById('id_booking_date');
    const timeSlotInput = document.getElementById('id_time_slot');
    const addressInput = document.getElementById('id_address');
    const serviceId = document.getElementById('service-id').value;

    if (timeSlotInput) {
        timeSlotInput.style.display = 'none';
    }

    $.getJSON(`/services/unavailable-dates/${serviceId}/`, function(data) {
        unavailableDates = data.fully_booked || [];

        const testDate = new Date('2025-06-18');
        const testDateStr = testDate.toISOString().split('T')[0];

        const year = testDate.getFullYear();
        const month = String(testDate.getMonth() + 1).padStart(2, '0');
        const day = String(testDate.getDate()).padStart(2, '0');
        const manualDateStr = `${year}-${month}-${day}`;

        if (data.partially_booked && Array.isArray(data.partially_booked)) {
            data.partially_booked.forEach(function(item) {
                if (!partiallyBookedSlots[item.date]) {
                    partiallyBookedSlots[item.date] = [];
                }
                partiallyBookedSlots[item.date].push(item.slot);
            });

            Object.keys(partiallyBookedSlots).forEach(function(date) {
                if (partiallyBookedSlots[date].includes('morning') && 
                    partiallyBookedSlots[date].includes('afternoon')) {
                    if (!unavailableDates.includes(date)) {
                        unavailableDates.push(date);
                    }
                }
            });
        }

        initializeDatepicker();
    });

    function initializeDatepicker() {
        $('#booking-datepicker').datepicker({
            format: 'yyyy-mm-dd',
            startDate: new Date(new Date().setDate(new Date().getDate() + 1)),
            endDate: new Date(new Date().setDate(new Date().getDate() + 60)),
            daysOfWeekDisabled: '0',
            autoclose: true,
            todayHighlight: true,
            beforeShowDay: function(date) {
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                const dateStr = `${year}-${month}-${day}`;

                if (unavailableDates.includes(dateStr)) {
                    return {
                        enabled: false,
                        classes: 'unavailable',
                        tooltip: 'Fully booked'
                    };
                }
                return true;
            }
        }).on('changeDate', function(e) {
            if (e && e.date) {
                selectedDate = e.format('yyyy-mm-dd');
                bookingDateInput.value = selectedDate;
                
                if (unavailableDates.includes(selectedDate)) {
                    alert("Sorry, this date is fully booked.");
                    return;
                }
                updateTimeSlots(selectedDate);
            }
        });
    }

    document.querySelectorAll('.time-slot').forEach(function(slot) {
        slot.addEventListener('click', function() {
            if (this.classList.contains('unavailable')) {
                return;
            }

            document.querySelectorAll('.time-slot').forEach(function(s) {
                s.classList.remove('selected');
            });

            this.classList.add('selected');
            timeSlotInput.value = this.getAttribute('data-value');
        });
    });

    function updateTimeSlots(date) {
        if (unavailableDates.includes(date)) {
            document.querySelectorAll('.time-slot').forEach(function(slot) {
                slot.classList.add('unavailable');
            });

            if (timeSlotInput) timeSlotInput.value = '';
            alert("Sorry, this date is fully booked. Please select another date.");
            return;
        }

        document.querySelectorAll('.time-slot').forEach(function(slot) {
            slot.classList.remove('unavailable', 'selected');
        });

        if (partiallyBookedSlots[date]) {
            partiallyBookedSlots[date].forEach(function(slot) {
                const slotElement = document.querySelector(`.time-slot[data-value="${slot}"]`);
                if (slotElement) {
                    slotElement.classList.add('unavailable');
                }
            });
        }

        const availableSlots = document.querySelectorAll('.time-slot:not(.unavailable)');
        if (document.querySelectorAll('.time-slot.selected').length === 0 && availableSlots.length > 0) {
            availableSlots[0].click();
        }
    }

    document.getElementById('booking-form').addEventListener('submit', function(e) {
        if (!selectedDate) {
            e.preventDefault();
            alert('Please select a date for your booking.');
            return false;
        }
        
        if (timeSlotInput.value === '') {
            e.preventDefault();
            alert('Please select a time slot for your booking.');
            return false;
        }

        if (addressInput.value.trim() === '') {
            e.preventDefault();
            alert('Please enter an address where we should meet you.');
            return false;
        }

        if (unavailableDates.includes(selectedDate)) {
            e.preventDefault();
            alert('Sorry, this date is fully booked. Please select another date.');
            return false;
        }
    });
});