from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination, ReviewDestination


REVIEW_DESTINATION_URL = reverse("TravelMore:review-destinations-list")


def sample_destination(**params):
    defaults = {
        "name": "South",
        "country": "USA",
    }
    defaults.update(params)

    return Destination.objects.create(**defaults)


class UnauthenticatedReviewDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(REVIEW_DESTINATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReviewDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_review_destination(self):
        destination = sample_destination()

        payload = {
            "text": "Great",
            "destination": destination.id,
        }

        response = self.client.post(REVIEW_DESTINATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review_destination = ReviewDestination.objects.get(id=response.data["id"])

        for key in payload:
            if key == "text":
                self.assertEqual(payload[key], getattr(review_destination, key))
            else:
                self.assertEqual(payload[key], getattr(review_destination, key).id)
