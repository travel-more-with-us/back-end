from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from TravelMore.models import (
    Destination, Stay, Accommodation
)


ACCOMMODATION_FRAME_URL = reverse("TravelMore:room-frames-list")


def sample_destination(**params):
    defaults = {
        "name": "South",
        "country": "USA",
    }
    defaults.update(params)

    return Destination.objects.create(**defaults)


def sample_stay(**params):
    destination = sample_destination()

    defaults = {
        "name": "Hotel",
        "destination": destination,
    }
    defaults.update(params)

    return Stay.objects.create(**defaults)


def sample_accommodation(**params):
    stay = sample_stay()

    defaults = {
        "name": "Hotel",
        "stay": stay,
    }
    defaults.update(params)

    return Accommodation.objects.create(**defaults)


class UnauthenticatedAccommodationFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ACCOMMODATION_FRAME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAccommodationFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_accommodation_frame_forbidden(self):
        rooms = sample_accommodation()
        payload = {
            "title": "Room Frame",
            "rooms": rooms,
        }

        response = self.client.post(ACCOMMODATION_FRAME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAccommodationFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)
