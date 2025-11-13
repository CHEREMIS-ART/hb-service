from datetime import date

import pytest
from django.core.exceptions import ValidationError

from hbservice.bookings.models import Booking
from hbservice.hotels.models import HotelRoom


@pytest.mark.django_db
class TestBookingModel:
    def test_create_booking_success(self):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)
        booking = Booking.objects.create(
            room=room, date_start=date(2024, 1, 1), date_end=date(2024, 1, 5)
        )

        assert booking.id is not None
        assert booking.room == room
        assert booking.date_start == date(2024, 1, 1)
        assert booking.date_end == date(2024, 1, 5)

    def test_booking_invalid_dates(self):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)
        booking = Booking(
            room=room, date_start=date(2024, 1, 5), date_end=date(2024, 1, 1)
        )

        with pytest.raises(ValidationError, match="End date must be after start date"):
            booking.full_clean()
