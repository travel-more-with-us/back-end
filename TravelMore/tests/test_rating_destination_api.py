from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination, RatingStar, RatingDestination


RATING_DESTINATION_URL = reverse("TravelMore:rating-destinations-list")


def sample_destination(**params):
    defaults = {
        "name": "South",
        "country": "USA",
    }
    defaults.update(params)

    return Destination.objects.create(**defaults)


def sample_star(**params):
    defaults = {
        "value": 5,
    }
    defaults.update(params)

    return RatingStar.objects.create(**defaults)


class UnauthenticatedRatingDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RATING_DESTINATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRatingDestinationApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_rating_destination(self):
        destination = sample_destination()
        star = sample_star()

        payload = {
            "star": star,
            "destination": destination.id,
        }

        response = self.client.post(RATING_DESTINATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating_destination = RatingDestination.objects.get(
            user=self.user, destination=destination
        )

        for key in payload:
            if key == "star":
                self.assertEqual(payload[key], getattr(rating_destination, key))
            else:
                self.assertEqual(payload[key], getattr(rating_destination, key).id)
