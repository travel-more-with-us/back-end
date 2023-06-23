from rest_framework import serializers
from models import Destination, Stay, Booking


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'country', 'description', 'review_number', 'rating']


class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = ['id', 'name', 'description', 'amenities']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'arrival_date', 'departure_date', 'number_of_guests', 'night_price', 'total_price']
        read_only_fields = ['total_price']
