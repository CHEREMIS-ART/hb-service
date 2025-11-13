from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room_id", "date_start", "date_end"]


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ["room_id", "date_start", "date_end"]

    def validate(self, data):
        room_id = data["room_id"]
        date_start = data["date_start"]
        date_end = data["date_end"]

        if date_start >= date_end:
            raise serializers.ValidationError("End date must be after start date")

        overlapping_bookings = Booking.objects.filter(
            room_id=room_id, date_start__lt=date_end, date_end__gt=date_start
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Room is alredy booked for these dates")

        return data
