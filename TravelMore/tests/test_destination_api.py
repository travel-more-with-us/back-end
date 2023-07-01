from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination
from TravelMore.serializers import (
    DestinationListSerializer,
    DestinationDetailSerializer,
)


DESTINATION_URL = reverse("TravelMore:destinations-list")


def sample_destination(**params):

    defaults = {
        "name": "South",
        "country": "USA",
    }
    defaults.update(params)

    return Destination.objects.create(**defaults)


def detail_url(destination_id):
    return reverse("TravelMore:destinations-detail", args=[destination_id])


class UnauthenticatedDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(DESTINATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_destinations(self):
        sample_destination()
        sample_destination()

        response = self.client.get(DESTINATION_URL)

        destinations = Destination.objects.all()
        serializer = DestinationListSerializer(destinations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, serializer.data)

    def test_retrieve_destination_detail(self):
        destination = sample_destination()

        url = detail_url(destination.id)
        response = self.client.get(url)

        serializer = DestinationDetailSerializer(destination)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_destination_by_name(self):
        destination = sample_destination()

        response = self.client.get(DESTINATION_URL, {"name": "Place"})

        serializer = DestinationListSerializer(destination)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer.data, response.data)

    def test_filter_destination_by_country(self):
        destination = sample_destination()

        response = self.client.get(DESTINATION_URL, {"name": "Canada"})

        serializer = DestinationListSerializer(destination)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer.data, response.data)


class AuthenticatedDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_destination_forbidden(self):
        payload = {
            "name": "South",
            "country": "USA"
        }

        response = self.client.post(DESTINATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com", "adminpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_destination(self):
        payload = {"name": "South", "country": "USA"}

        response = self.client.post(DESTINATION_URL, payload)

        destination = Destination.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(destination, key))
