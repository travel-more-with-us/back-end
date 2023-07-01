from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Stay, Destination
from TravelMore.serializers import StayDetailSerializer, StayListSerializer

STAY_URL = reverse("TravelMore:stays-list")


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


def detail_url(stay_id):
    return reverse("TravelMore:stays-detail", args=[stay_id])


class UnauthenticatedStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(STAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_stays(self):
        sample_stay()
        sample_stay()

        response = self.client.get(STAY_URL)

        stays = Stay.objects.all()
        serializer = StayListSerializer(stays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, serializer.data)

    def test_retrieve_stay_detail(self):
        stay = sample_stay()

        url = detail_url(stay.id)
        response = self.client.get(url)

        serializer = StayDetailSerializer(stay)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_stay_by_name(self):
        stay = sample_stay()

        response = self.client.get(STAY_URL, {"name": "Standard"})

        serializer = StayListSerializer(stay)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer.data, response.data)


class AuthenticatedStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_create_stay_forbidden(self):
        destination = sample_destination()
        payload = {
            "name": "Hotel_1",
            "destination": destination
        }

        response = self.client.post(STAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_stay(self):
        destination = sample_destination()
        payload = {
            "name": "Hotel_1",
            "destination": destination.id
        }

        response = self.client.post(STAY_URL, payload)

        stay = Stay.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key == "destination":
                self.assertEqual(payload[key], getattr(stay, key).id)
            else:
                self.assertEqual(payload[key], getattr(stay, key))
