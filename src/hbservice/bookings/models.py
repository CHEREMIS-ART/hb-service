from django.core.exceptions import ValidationError
from django.db import models

from hbservice.hotels.models import HotelRoom


class Booking(models.Model):
    room = models.ForeignKey(
        HotelRoom, on_delete=models.CASCADE, related_name="booking"
    )
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        indexes = [
            models.Index(fields=["room", "date_start"]),
            models.Index(fields=["date_start", "date_end"]),
        ]

    def clean(self):
        if self.date_start >= self.date_end:
            raise ValidationError("End date must be after start date")
