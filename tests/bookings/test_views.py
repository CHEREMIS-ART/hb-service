from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from hbservice.bookings.models import Booking
from hbservice.hotels.models import HotelRoom


@pytest.mark.django_db
class TestBookingViews:
    def test_create_booking_success(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)

        data = {
            "room_id": room.id,
            "date_start": "2024-01-01",
            "date_end": "2024-01-05",
        }

        response = client.post(reverse("create_booking"), data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "booking_id" in response.data
        assert Booking.objects.count() == 1

    def test_create_booking_room_not_found(self, client):
        data = {
            "room_id": 999,
            "date_start": "2024-01-01",
            "date_end": "2024-01-05",
        }

        response = client.post(reverse("create_booking"), data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Room not found"

    def test_create_booking_overlapping_dates(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)

        Booking.objects.create(
            room=room, date_start=date(2024, 1, 1), date_end=date(2024, 1, 5)
        )

        data = {
            "room_id": room.id,
            "date_start": "2024-01-03",
            "date_end": "2024-01-07",
        }

        response = client.post(reverse("create_booking"), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Room is alredy booked for these dates" in str(response.data)

    def test_create_booking_invalid_dates(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)

        data = {
            "room_id": room.id,
            "date_start": "2024-01-05",
            "date_end": "2024-01-01",
        }

        response = client.post(reverse("create_booking"), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "End date must be after start date" in str(response.data)

    def test_list_bookings_success(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)

        booking1 = Booking.objects.create(
            room=room, date_start=date(2024, 1, 1), date_end=date(2024, 1, 5)
        )
        booking2 = Booking.objects.create(
            room=room, date_start=date(2024, 1, 10), date_end=date(2024, 1, 15)
        )

        response = client.get(reverse("list_bookings"), {"room_id": room.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["id"] == booking1.id
        assert response.data[1]["id"] == booking2.id

    def test_list_bookings_missing_room_id(self, client):
        response = client.get(reverse("list_bookings"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "room_id parameter is required"

    def test_list_bookings_invalid_room_id(self, client):
        response = client.get(reverse("list_bookings"), {"room_id": "invalid"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid room_id"

    def test_delete_booking_success(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)
        booking = Booking.objects.create(
            room=room, date_start=date(2024, 1, 1), date_end=date(2024, 1, 5)
        )

        response = client.delete(
            reverse("delete_booking", kwargs={"booking_id": booking.id})
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Booking.objects.filter(id=booking.id).exists()

    def test_delete_booking_not_found(self, client):
        response = client.delete(reverse("delete_booking", kwargs={"booking_id": 999}))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Booking not found"
