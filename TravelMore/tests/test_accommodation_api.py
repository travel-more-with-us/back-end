from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Accommodation, Destination, Stay
from TravelMore.serializers import (
    AccommodationListSerializer,
    AccommodationDetailSerializer
)


ACCOMMODATION_URL = reverse("TravelMore:accommodations-list")


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


def detail_url(accommodation_id):
    return reverse("TravelMore:accommodations-detail", args=[accommodation_id])


class UnauthenticatedAccommodationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ACCOMMODATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_accommodations(self):
        sample_accommodation()

        response = self.client.get(ACCOMMODATION_URL)

        rooms = Accommodation.objects.all()
        serializer = AccommodationListSerializer(rooms, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_accommodation_detail(self):
        room = sample_accommodation()

        url = detail_url(room.id)
        response = self.client.get(url)

        serializer = AccommodationDetailSerializer(room)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_accommodations_by_name(self):
        room1 = sample_accommodation(name="Standard")
        room2 = sample_accommodation(name="Junior Suite")
        room3 = sample_accommodation(name="Suite")

        response = self.client.get(ACCOMMODATION_URL, {"name": "suite"})

        serializer1 = AccommodationListSerializer(room1)
        serializer2 = AccommodationListSerializer(room2)
        serializer3 = AccommodationListSerializer(room3)

        self.assertNotIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertIn(serializer3.data, response.data)


class AuthenticatedAccommodationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_accommodation_forbidden(self):
        stay = sample_stay()
        payload = {
            "name": "Hotel",
            "stay": stay
        }

        response = self.client.post(ACCOMMODATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAccommodationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_accommodation(self):
        stay = sample_stay()
        payload = {
            "name": "Hotel",
            "stay": stay.id
        }

        response = self.client.post(ACCOMMODATION_URL, payload)

        room = Accommodation.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key == "stay":
                self.assertEqual(payload[key], getattr(room, key).id)
            else:
                self.assertEqual(payload[key], getattr(room, key))
