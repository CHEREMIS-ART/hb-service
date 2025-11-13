from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hbservice.hotels.models import HotelRoom

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


@api_view(["POST"])
def create_booking(request):
    serializer = BookingCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            HotelRoom.objects.get(id=serializer.validated_data["room_id"])
        except HotelRoom.DoesNotExist:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        booking = serializer.save()
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Booking.DoesNotExist:
        return Response(
            {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def list_bookings(request):
    room_id = request.GET.get("room_id")
    if not room_id:
        return Response(
            {"error": "room_id parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        bookings = Booking.objects.filter(room_id=room_id).order_by("date_start")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except ValueError:
        return Response(
            {"error": "Invalid room_id"}, status=status.HTTP_400_BAD_REQUEST
        )
