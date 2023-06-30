import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from TravelMore.models import (
    Amenity,
    Destination,
    Stay,
    StayFrames,
    RatingStar,
    RatingStay,
    RatingDestination,
    ReviewStay,
    ReviewDestination,
    Accommodation,
    AccommodationFrames,
    Booking,
)


class AmenityModelTest(TestCase):

    def test_amenity_str(self):
        amenity = Amenity.objects.create(name="Wi-Fi")

        self.assertEqual(str(amenity), f"{amenity.name}")


class DestinationModelTest(TestCase):

    def test_destination_str(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )

        self.assertEqual(
            str(destination), f"{destination.name}, {destination.country}"
        )


class StayModelTest(TestCase):

    def test_stay_str(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(
            name="Hotel", destination=destination
        )

        self.assertEqual(str(stay), f"{stay.name}")


class StayFramesModelTest(TestCase):

    def test_stay_frames_str(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stays = Stay.objects.create(name="Hotel", destination=destination)
        stay_frame = StayFrames.objects.create(title="Hotel_1", stays=stays)

        self.assertEqual(str(stay_frame), f"{stay_frame.title}")


class RatingStarModelTest(TestCase):

    def test_rating_star_str(self):
        rating_star = RatingStar.objects.create(value=1)

        self.assertEqual(str(rating_star), f"{rating_star.value}")


class RatingStayModelTest(TestCase):

    def test_rating_stay_str(self):
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        star = RatingStar.objects.create(value=1)
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)

        rating_stay = RatingStay.objects.create(
            user=user, stay=stay, star=star
        )

        self.assertEqual(
            str(rating_stay), f"{rating_stay.star} - {rating_stay.stay}"
        )


class RatingDestinationModelTest(TestCase):

    def test_rating_destination_str(self):
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        star = RatingStar.objects.create(value=1)
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        rating_destination = RatingDestination.objects.create(
            user=user, destination=destination, star=star
        )

        self.assertEqual(
            str(rating_destination),
            f"{rating_destination.star} - {rating_destination.destination}",
        )


class ReviewStayModelTest(TestCase):

    def test_review_stay_str(self):
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        review_stay = ReviewStay.objects.create(
            user=user, stay=stay, text="Test review for the stay"
        )

        self.assertEqual(str(review_stay), f"{review_stay.user} - {review_stay.stay}")


class ReviewDestinationModelTest(TestCase):

    def test_review_destination_str(self):
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        review_destination = ReviewDestination.objects.create(
            user=user, destination=destination, text="Test review for the destination"
        )

        self.assertEqual(
            str(review_destination),
            f"{review_destination.user} - {review_destination.destination}",
        )


class AccommodationModelTest(TestCase):

    def test_accommodation_str(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        room = Accommodation.objects.create(name="Standard", stay=stay)

        self.assertEqual(str(room), f"{room.name}")

    def test_accommodation_defaults(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        room = Accommodation.objects.create(name="Standard", stay=stay)

        self.assertEqual(room.type_room, "STANDARD")
        self.assertEqual(room.number_rooms, "ONE ROOM")
        self.assertEqual(room.number_beds, "SINGLE-BED")
        self.assertIsNone(room.night_price)
        self.assertFalse(room.is_booked)

    def test_accommodation_amenities(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        room = Accommodation.objects.create(name="Standard", stay=stay)
        amenity1 = Amenity.objects.create(name="WiFi")
        amenity2 = Amenity.objects.create(name="Swimming Pool")

        room.amenities.add(amenity1, amenity2)

        self.assertEqual(room.amenities.count(), 2)
        self.assertIn(amenity1, room.amenities.all())
        self.assertIn(amenity2, room.amenities.all())

    def test_accommodation_reset_booking_status(self):
        user1 = get_user_model().objects.create_user(
            email="admin@user.com",
            username="Admin",
            password="admin12345",
            phone_number="+123456789",
        )
        user2 = get_user_model().objects.create_user(
            email="user@user.com",
            username="User",
            password="user12345",
            phone_number="+30123456789",
        )
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        room = Accommodation.objects.create(name="Standard", stay=stay)
        room.night_price = 100.00
        room.save()

        Booking.objects.create(
            arrival_date=datetime.date.today() - datetime.timedelta(days=3),
            departure_date=datetime.date.today() - datetime.timedelta(days=2),
            user=user1,
            number_of_guests=2,
            stay=stay,
            rooms=room,
        )
        Booking.objects.create(
            arrival_date=datetime.date.today() - datetime.timedelta(days=2),
            departure_date=datetime.date.today() - datetime.timedelta(days=1),
            user=user2,
            number_of_guests=3,
            stay=stay,
            rooms=room,
        )

        room.reset_booking_status()
        self.assertTrue(room.is_booked)

        booking_room = Booking.objects.filter(departure_date__lt=datetime.date.today())
        booking_room.update(
            departure_date=datetime.date.today() - datetime.timedelta(days=1)
        )

        room.reset_booking_status()
        self.assertFalse(room.is_booked)


class AccommodationFramesModelTest(TestCase):

    def test_accommodation_frame_str(self):
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        rooms = Accommodation.objects.create(name="Standard", stay=stay)
        room_frame = AccommodationFrames.objects.create(
            title="Standard_1", rooms=rooms
        )

        self.assertEqual(str(room_frame), f"{room_frame.title}")


class BookingModelTest(TestCase):

    def test_booking_str(self):
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        destination = Destination.objects.create(
            name="The Pacific Ocean", country="USA"
        )
        stay = Stay.objects.create(name="Hotel", destination=destination)
        rooms = Accommodation.objects.create(name="Standard", stay=stay)
        rooms.night_price = 100.00
        rooms.save()

        arrival_date = datetime.date.today() + datetime.timedelta(days=1)
        departure_date = datetime.date.today() + datetime.timedelta(days=2)
        booking = Booking.objects.create(
            user=user,
            stay=stay,
            rooms=rooms,
            number_of_guests=2,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )

        self.assertEqual(
            str(booking), f"Booking for {booking.number_of_guests} guests"
        )

    def test_calculate_total_price(self):

        user = get_user_model().objects.create_user(
            email="user@user.com",
            password="admin12345",
        )
        destination = Destination.objects.create(
            name="The Black Sea", country="USA"
        )
        stay = Stay.objects.create(name="Hotel_1", destination=destination)
        rooms = Accommodation.objects.create(name="Standard_1", stay=stay)
        rooms.night_price = 200.00
        rooms.save()

        arrival_date = datetime.date.today() + datetime.timedelta(days=1)
        departure_date = datetime.date.today() + datetime.timedelta(days=2)

        booking = Booking.objects.create(
            user=user,
            stay=stay,
            rooms=rooms,
            number_of_guests=2,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )

        nights = (booking.departure_date - booking.arrival_date).days
        expected_price = rooms.night_price * nights

        booking.calculate_total_price()
        self.assertEqual(booking.total_price, expected_price)

    def test_save_updates_total_price(self):
        user = get_user_model().objects.create_user(
            email="user@user.com",
            password="admin12345",
        )
        destination = Destination.objects.create(
            name="The North", country="USA"
        )
        stay = Stay.objects.create(name="Hotel_2", destination=destination)
        rooms = Accommodation.objects.create(name="Standard_2", stay=stay)
        rooms.night_price = 300.00
        rooms.save()

        arrival_date = datetime.date.today() + datetime.timedelta(days=1)
        departure_date = datetime.date.today() + datetime.timedelta(days=2)

        booking = Booking.objects.create(
            user=user,
            stay=stay,
            rooms=rooms,
            number_of_guests=2,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )
        booking.departure_date = datetime.date.today() + datetime.timedelta(days=3)
        booking.save()

        nights = (booking.departure_date - booking.arrival_date).days
        expected_price = rooms.night_price * nights

        self.assertEqual(booking.total_price, expected_price)
