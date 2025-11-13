import pytest
from django.urls import reverse
from rest_framework import status

from hbservice.hotels.models import HotelRoom


@pytest.mark.django_db
class TestHotelViews:
    def test_create_and_list_rooms(self, client):
        create_data = {"description": "Test Room", "price_per_night": "150.00"}
        create_response = client.post(reverse("create_room"), data=create_data)

        assert create_response.status_code == status.HTTP_201_CREATED
        room_id = create_response.data["room_id"]

        list_response = client.get(reverse("list_rooms"))

        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) == 1
        assert list_response.data[0]["id"] == room_id
        assert list_response.data[0]["description"] == "Test Room"

    def test_create_room_invalid_data(self, client):
        data = {"price_per_night": "100.00"}

        response = client.post(reverse("create_room"), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.data

    def test_delete_room(self, client):
        room = HotelRoom.objects.create(description="Test Room", price_per_night=100.00)

        delete_response = client.delete(
            reverse("delete_room", kwargs={"room_id": room.id})
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = client.get(reverse("list_rooms"))
        assert len(list_response.data) == 0

    def test_delete_nonexistent_room(self, client):
        response = client.delete(reverse("delete_room", kwargs={"room_id": 999}))
        assert response.status_code == status.HTTP_404_NOT_FOUND
