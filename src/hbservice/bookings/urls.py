from django.urls import path

from . import views

urlpatterns = [
    path("list", views.list_bookings, name="list_bookings"),
    path("create", views.create_booking, name="create_booking"),
    path("delete/<int:booking_id>", views.delete_booking, name="delete_booking"),
]
