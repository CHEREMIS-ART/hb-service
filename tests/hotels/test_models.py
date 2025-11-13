import pytest

from hbservice.hotels.models import HotelRoom


@pytest.mark.django_db
class TestHotelRoomModel:
    def test_create_room(self):
        """Тест создания комнаты"""
        room = HotelRoom.objects.create(
            description="Luxury suite with ocean view", price_per_night=250.00
        )
        assert room.description == "Luxury suite with ocean view"
        assert room.price_per_night == 250.00
        assert HotelRoom.objects.count() == 1

    def test_room_field_validation(self):
        """Тест валидации полей модели"""
        from decimal import Decimal

        room = HotelRoom(description="A" * 1000, price_per_night=Decimal("999999.99"))
        room.full_clean()
        room.save()
        assert HotelRoom.objects.count() == 1

    def test_room_default_values(self):
        """Тест автоматического заполнения created_at"""
        room = HotelRoom.objects.create(description="Test room", price_per_night=100.00)
        assert room.created_at is not None
        assert room.id is not None

    def test_price_boundaries(self):
        """Тест граничных значений цены"""
        cheap_room = HotelRoom.objects.create(
            description="Budget room", price_per_night=0.01
        )
        expensive_room = HotelRoom.objects.create(
            description="Luxury suite", price_per_night=9999999.99
        )
        assert cheap_room.price_per_night == 0.01
        assert expensive_room.price_per_night == 9999999.99

    def test_room_queryset_methods(self):
        """Тест методов запросов к базе данных"""
        HotelRoom.objects.create(description="Cheap room", price_per_night=50.00)
        HotelRoom.objects.create(description="Medium room", price_per_night=150.00)
        HotelRoom.objects.create(description="Expensive room", price_per_night=500.00)

        affordable_rooms = HotelRoom.objects.filter(price_per_night__lte=200.00)
        assert affordable_rooms.count() == 2

        from django.db.models import Avg

        avg_price = HotelRoom.objects.aggregate(avg_price=Avg("price_per_night"))
        assert avg_price["avg_price"] > 0
