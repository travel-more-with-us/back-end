import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings


class Amenity(models.Model):
    name = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "amenity"
        verbose_name_plural = "amenities"

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True,)
    url_map_destination = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Stay(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    image = models.ImageField(null=True,)
    url_map_stay = models.URLField(max_length=255, blank=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="stays"
    )
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return self.name


class StayFrames(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True)
    stays = models.ForeignKey(
        Stay, on_delete=models.CASCADE, related_name="stay_frames"
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Stay frame"
        verbose_name_plural = "Stay frames"

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        ordering = ("-value",)

    def __str__(self):
        return str(self.value)


class RatingStay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_rating_stay",
    )
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, related_name="star_rating_stay"
    )
    stay = models.ForeignKey(
        Stay, on_delete=models.CASCADE, related_name="stay_rating"
    )

    def __str__(self):
        return f"{self.star} - {self.stay}"


class RatingDestination(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_rating_destination",
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        related_name="star_rating_destination"
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="destination_rating"
    )

    def __str__(self):
        return f"{self.star} - {self.destination}"


class ReviewStay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_review_stay",
    )
    text = models.TextField(blank=True)
    stay = models.ForeignKey(
        Stay, on_delete=models.CASCADE, related_name="review_stays"
    )

    def __str__(self):
        return f"{self.user} - {self.stay}"


class ReviewDestination(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_review_destination",
    )
    text = models.TextField(blank=True)
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="review_destinations"
    )

    def __str__(self):
        return f"{self.user} - {self.destination}"


class Accommodation(models.Model):
    TYPE_ROOM_CHOICES = (
        ("STANDARD", "standard"),
        ("JUNIOR SUITE", "junior suite"),
        ("SUITE", "suite"),
    )

    NUMBER_ROOMS_CHOICES = (
        ("ONE ROOM", "one room"),
        ("TWO ROOM", "two room"),
        ("THREE ROOM", "three room"),
        ("FOUR ROOM", "four room"),
    )

    NUMBER_BEDS_CHOICES = (
        ("SINGLE-BED", "single-bed"),
        ("DOUBLE-BED", "double-bed"),
        ("TRIPLE-BED", "triple-bed"),
        ("FOUR-BED", "four-bed"),
        ("FIVE-BED", "five-bed"),
        ("SIX-BED", "six-bed"),
        ("EIGHT-BED", "eight-bed"),
    )

    name = models.CharField(max_length=255, unique=True)
    type_room = models.CharField(
        max_length=255, choices=TYPE_ROOM_CHOICES, default="STANDARD"
    )
    number_rooms = models.CharField(
        max_length=100, choices=NUMBER_ROOMS_CHOICES, default="ONE ROOM"
    )
    number_beds = models.CharField(
        max_length=100, choices=NUMBER_BEDS_CHOICES, default="SINGLE-BED"
    )
    night_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(null=True)
    stay = models.ForeignKey(
        Stay,
        on_delete=models.CASCADE,
        related_name="accommodations",
        null=True,
        blank=True,
    )
    amenities = models.ManyToManyField(Amenity, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def reset_booking_status(self):
        now = timezone.now().date()
        if self.booking_room.exclude(
            departure_date__lt=now, rooms__is_booked=True
        ).exists():
            self.is_booked = True
        else:
            self.is_booked = False
        self.save()


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_booking",
    )
    arrival_date = models.DateField()
    departure_date = models.DateField()
    number_of_guests = models.IntegerField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True
    )
    stay = models.ForeignKey(
        Stay, on_delete=models.CASCADE, related_name="booking_stay"
    )
    rooms = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name="booking_room",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)
        self.rooms.reset_booking_status()

    def calculate_total_price(self):
        nights = (self.departure_date - self.arrival_date).days

        room_price = self.rooms.night_price

        self.total_price = room_price * nights

    def __str__(self):
        return f"Booking for {self.number_of_guests} guests"
