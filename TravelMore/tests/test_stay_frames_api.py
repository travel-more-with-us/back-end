from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from TravelMore.models import Destination, Stay, StayFrames


STAY_FRAME_URL = reverse("TravelMore:stay-frames-list")


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


def sample_stay_frame(**params):
    stays = sample_stay()

    defaults = {
        "title": "Sample room frame",
        "stays": stays
    }
    defaults.update(params)

    return StayFrames.objects.create(**defaults)


class UnauthenticatedStayFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(STAY_FRAME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedStayFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_stay_frame_forbidden(self):
        stays = sample_stay()
        payload = {
            "title": "Stay Frame",
            "stays": stays,
        }

        response = self.client.post(STAY_FRAME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminStayFrameApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_stay_frame(self):
        stay_frame = sample_stay_frame()
        stay = sample_stay()

        payload = {
            "title": stay_frame.title,
            "stays": stay.id,
        }

        response = self.client.post(STAY_FRAME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        frame = StayFrames.objects.get(
            title=response.data["title"], stays=stay.id
        )

        for key in payload:
            if key == "stays":
                self.assertEqual(int(payload[key]), getattr(frame, key).id)
            else:
                self.assertEqual(payload[key], str(getattr(frame, key)))
