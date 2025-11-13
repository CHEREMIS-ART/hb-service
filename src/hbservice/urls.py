from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hotels/", include("hbservice.hotels.urls")),
    path("bookings/", include("hbservice.bookings.urls")),
]
