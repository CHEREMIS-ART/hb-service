from django.urls import path

from . import views

urlpatterns = [
    path("list", views.list_rooms, name="list_rooms"),
    path("create", views.create_room, name="create_room"),
    path("delete/<int:room_id>", views.delete_room, name="delete_room"),
]
