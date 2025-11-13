from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import HotelRoom
from .serializers import HotelRoomCreateSerializer, HotelRoomSerializer


@api_view(["POST"])
def create_room(request):
    serializer = HotelRoomCreateSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_room(request, room_id):
    try:
        with transaction.atomic():
            room = HotelRoom.objects.get(id=room_id)
            room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except HotelRoom.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_rooms(request):
    sort_by = request.GET.get("sort_by", "id")
    order = request.GET.get("order", "asc")

    valid_sort_fields = ["price_per_night", "created_at", "id"]
    if sort_by not in valid_sort_fields:
        sort_by = "id"

    if order == "desc":
        sort_by = f"-{sort_by}"

    rooms = HotelRoom.objects.all().order_by(sort_by)
    serializer = HotelRoomSerializer(rooms, many=True)
    return Response(serializer.data)
