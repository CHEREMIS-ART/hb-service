import os
import sys

import django
import pytest
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def pytest_configure():
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "rest_framework",
                "hbservice.hotels",
                "hbservice.bookings",
            ],
            SECRET_KEY="test-secret-key",
            USE_TZ=True,
            ROOT_URLCONF="hbservice.urls",
            ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"],
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ],
        )
        django.setup()

    from django.core.management import call_command

    call_command("migrate", verbosity=0)


pytest_configure()


@pytest.fixture(autouse=True)
def clean_database():
    from hbservice.bookings.models import Booking
    from hbservice.hotels.models import HotelRoom

    HotelRoom.objects.all().delete()
    Booking.objects.all().delete()


@pytest.fixture
def client():
    from django.test import Client

    return Client()
