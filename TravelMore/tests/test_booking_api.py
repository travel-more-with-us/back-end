import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from TravelMore.models import Destination, Stay, Accommodation, Booking
from TravelMore.serializers import BookingListSerializer


BOOKING_URL = reverse("TravelMore:bookings-list")


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
        "name": "Conkord",
        "destination": destination,
    }
    defaults.update(params)

    return Stay.objects.create(**defaults)


def sample_accommodation(**params):
    stay = sample_stay()

    defaults = {
        "name": "Standard",
        "stay": stay,
    }
    defaults.update(params)

    return Accommodation.objects.create(**defaults)


def sample_booking(**params):
    stay = sample_stay()
    rooms = sample_accommodation()
    rooms.night_price = 100.00
    rooms.save()

    arrival_date = datetime.date.today() + datetime.timedelta(days=1)
    departure_date = datetime.date.today() + datetime.timedelta(days=2)

    defaults = {
        "rooms": rooms,
        "stay": stay,
        "number_of_guests": 2,
        "arrival_date": arrival_date,
        "departure_date": departure_date
    }

    defaults.update(params)

    return Booking.objects.create(**defaults)


class UnauthenticatedBookingApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BOOKING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookingApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_bookings(self):
        user = self.user
        sample_booking(user=user)

        response = self.client.get(BOOKING_URL)

        booking = Booking.objects.all()
        serializer = BookingListSerializer(booking, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_booking(self):
        user = self.user
        destination = Destination.objects.create(name="City")
        hotel = Stay.objects.create(name="Hotel", destination=destination)
        room = Accommodation.objects.create(name="Suite", stay=hotel)
        room.night_price = 100.00
        room.save()
        arrival_date = datetime.date.today() + datetime.timedelta(days=3)
        departure_date = datetime.date.today() + datetime.timedelta(days=5)

        payload = {
            "user": user.id,
            "rooms": room.id,
            "stay": hotel.id,
            "number_of_guests": 2,
            "arrival_date": arrival_date,
            "departure_date": departure_date
        }

        response = self.client.post(BOOKING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = Booking.objects.get(id=response.data["id"])

        for key in payload:
            if key in ("rooms", "user", "stay"):
                self.assertEqual(payload[key], getattr(booking, key).id)
            else:
                self.assertEqual(payload[key], getattr(booking, key))
