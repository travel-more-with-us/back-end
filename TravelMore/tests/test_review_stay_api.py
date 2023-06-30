from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination, Stay, ReviewStay

REVIEW_STAY_URL = reverse("TravelMore:review-stays-list")


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


class UnauthenticatedReviewStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(REVIEW_STAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReviewStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_review_stay(self):
        stay = sample_stay()

        payload = {
            "text": "Great",
            "stay": stay.id,
        }

        response = self.client.post(REVIEW_STAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review_stay = ReviewStay.objects.get(id=response.data["id"])

        for key in payload:
            if key == "text":
                self.assertEqual(payload[key], getattr(review_stay, key))
            else:
                self.assertEqual(payload[key], getattr(review_stay, key).id)
