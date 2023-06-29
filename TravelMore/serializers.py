from rest_framework import serializers
from TravelMore.models import (
    Destination,
    Stay,
    StayFrames,
    Booking,
    Amenity,
    RatingDestination,
    RatingStar,
    RatingStay,
    ReviewStay,
    ReviewDestination,
    Accommodation,
    AccommodationFrames,
)
from user.serializers import UserListSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("id", "name",)


class RatingDestinationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="first_name", read_only=True)
    star = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = RatingDestination
        fields = ("user", "star")


class RatingDestinationCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    star = serializers.SlugRelatedField(
        slug_field="value", queryset=RatingStar.objects.all()
    )

    class Meta:
        model = RatingDestination
        fields = ("user", "star", "destination")

    def create(self, validated_data):
        rating, created = RatingDestination.objects.update_or_create(
            user=validated_data.get("user", None),
            destination=validated_data.get("destination", None),
            defaults={"star": validated_data.get("star")},
        )

        return rating


class RatingStaySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="first_name", read_only=True)
    star = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = RatingStay
        fields = ("user", "star")


class RatingStayCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    star = serializers.SlugRelatedField(
        slug_field="value", queryset=RatingStar.objects.all()
    )

    class Meta:
        model = RatingStay
        fields = ("user", "star", "stay")

    def create(self, validated_data):
        rating, created = RatingStay.objects.update_or_create(
            user=validated_data.get("user", None),
            stay=validated_data.get("stay", None),
            defaults={"star": validated_data.get("star")},
        )

        return rating


class ReviewStaySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="first_name", read_only=True)

    class Meta:
        model = ReviewStay
        fields = (
            "id",
            "user",
            "text",
        )


class ReviewDestinationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="first_name", read_only=True)

    class Meta:
        model = ReviewDestination
        fields = (
            "id",
            "user",
            "text",
        )


class AccommodationFramesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccommodationFrames
        fields = ("id", "title", "rooms", "image")


class AccommodationFramesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccommodationFrames
        fields = ("id", "image")


class AccommodationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accommodation
        fields = (
            "id",
            "name",
            "stay",
            "type_room",
            "number_rooms",
            "number_beds",
            "amenities",
        )


class AccommodationListSerializer(serializers.ModelSerializer):
    amenities = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    stay = serializers.CharField(read_only=True, source="stay.name")

    class Meta:
        model = Accommodation
        fields = (
            "id",
            "name",
            "stay",
            "type_room",
            "number_rooms",
            "number_beds",
            "amenities",
            "image",
        )


class AccommodationDetailSerializer(serializers.ModelSerializer):
    room_frames = AccommodationFramesListSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    stay = serializers.CharField(read_only=True, source="stay.name")

    class Meta:
        model = Accommodation
        fields = (
            "id",
            "name",
            "stay",
            "type_room",
            "number_rooms",
            "number_beds",
            "amenities",
            "image",
            "room_frames"
        )


class AccommodationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accommodation
        fields = ("id", "image")


class StayFramesSerializer(serializers.ModelSerializer):

    class Meta:
        model = StayFrames
        fields = ("id", "title", "stays", "image")


class StayFramesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StayFrames
        fields = ("id", "image")


class StaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Stay
        fields = (
            "id",
            "name",
            "destination",
            "address",
            "description",
            "url_map_stay",
            "amenities",
        )


class StayListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.IntegerField(read_only=True)
    reviews_count = serializers.SerializerMethodField()
    name_destination = serializers.CharField(read_only=True, source="destination.name")
    country_destination = serializers.CharField(read_only=True, source="destination.country")

    class Meta:
        model = Stay
        fields = (
            "id",
            "name",
            "name_destination",
            "country_destination",
            "image",
            "avg_rating",
            "reviews_count"
        )

    def get_reviews_count(self, obj):
        return obj.review_stays.count()


class StayDetailSerializer(serializers.ModelSerializer):
    review_stays = ReviewStaySerializer(many=True, read_only=True)
    rooms = AccommodationListSerializer(many=True, read_only=True)
    amenities = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    stay_frames = StayFramesListSerializer(many=True, read_only=True)
    country = serializers.CharField(read_only=True, source="destination.country")

    class Meta:
        model = Stay
        fields = (
            "id",
            "name",
            "country",
            "address",
            "image",
            "stay_frames",
            "description",
            "rooms",
            "url_map_stay",
            "amenities",
            "review_stays"
        )


class StayImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stay
        fields = ("id", "image")


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = (
            "id",
            "name",
            "country",
            "description",
            "url_map_destination",
        )


class DestinationListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.IntegerField(read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = (
            "id",
            "name",
            "country",
            "image",
            "avg_rating",
            "reviews_count"
        )

    def get_reviews_count(self, obj):
        return obj.review_destinations.count()


class DestinationDetailSerializer(serializers.ModelSerializer):
    stays = StayDetailSerializer(many=True, read_only=True)
    review_destinations = ReviewDestinationSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = (
            "id",
            "name",
            "country",
            "image",
            "description",
            "url_map_destination",
            "stays",
            "review_destinations"
        )


class DestinationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ("id", "image")


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = (
            "id",
            "user",
            "arrival_date",
            "departure_date",
            "number_of_guests",
            "stay",
            "rooms",
            "night_price",
            "total_price",
        )
        read_only_fields = ["total_price"]


class BookingListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    stay = StayListSerializer(read_only=True)
    rooms = AccommodationListSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "user",
            "arrival_date",
            "departure_date",
            "number_of_guests",
            "stay",
            "rooms",
            "night_price",
            "total_price",
        )
