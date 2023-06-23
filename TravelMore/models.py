from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    description = models.TextField()
    review_number = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.name


class Stay(models.Model):
    AMENITIES_CHOICES = [
        ('wifi', 'Wi-Fi'),
        ('parking', 'Parking'),
        ('pool', 'Swimming Pool'),
        ('balcony', 'Balcony'),
        ('restaurant', 'Restaurant'),
    ]

    name = models.CharField(max_length=63)
    description = models.TextField()
    amenities = models.CharField(max_length=20, choices=AMENITIES_CHOICES, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    arrival_date = models.DateField()
    departure_date = models.DateField()
    number_of_guests = models.IntegerField()
    night_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        nights = (self.departure_date - self.arrival_date).days
        self.total_price = self.night_price * nights

    def __str__(self):
        return f'Booking for {self.number_of_guests} guests'

