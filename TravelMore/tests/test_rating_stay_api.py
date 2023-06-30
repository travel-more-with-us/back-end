from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination, Stay, RatingStar, RatingStay


RATING_STAY_URL = reverse("TravelMore:rating-stays-list")


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


def sample_star(**params):
    defaults = {
        "value": 3,
    }
    defaults.update(params)

    return RatingStar.objects.create(**defaults)


class UnauthenticatedRatingStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RATING_STAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRatingStayApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_rating_stay(self):
        stay = sample_stay()
        star = sample_star()

        payload = {
            "star": star,
            "stay": stay.id,
        }

        response = self.client.post(RATING_STAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating_stay = RatingStay.objects.get(user=self.user, stay=stay)

        for key in payload:
            if key == "star":
                self.assertEqual(payload[key], getattr(rating_stay, key))
            else:
                self.assertEqual(payload[key], getattr(rating_stay, key).id)
