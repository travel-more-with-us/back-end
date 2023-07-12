from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from TravelMore.models import (
    Destination,
    Stay,
    StayFrames,
    Accommodation,
    Amenity,
    Booking,
)
from TravelMore.permissions import IsAdminOrReadOnly
from TravelMore.serializers import (
    DestinationSerializer,
    DestinationListSerializer,
    DestinationDetailSerializer,
    DestinationImageSerializer,
    StaySerializer,
    StayListSerializer,
    StayDetailSerializer,
    StayImageSerializer,
    StayFramesSerializer,
    BookingSerializer,
    BookingListSerializer,
    RatingDestinationCreateSerializer,
    RatingStayCreateSerializer,
    AccommodationSerializer,
    AccommodationListSerializer,
    AccommodationDetailSerializer,
    AccommodationImageSerializer,
    ReviewDestinationSerializer,
    ReviewStaySerializer,
    AmenitySerializer,
)


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = (
        Destination.objects.annotate(
            average_rating=Cast(
                Avg("destination_rating__star__value"),
                IntegerField()
            )
        )
    )
    serializer_class = DestinationSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the destinations with filters"""
        name = self.request.query_params.get("name")
        country = self.request.query_params.get("country")
        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if country:
            queryset = queryset.filter(country__icontains=country)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return DestinationListSerializer
        if self.action == "retrieve":
            return DestinationDetailSerializer
        if self.action == "upload_image":
            return DestinationImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific destination"""
        destination = self.get_object()
        serializer = self.get_serializer(destination, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by destination name (ex. ?name=South America)",
            ),
            OpenApiParameter(
                "country",
                type=OpenApiTypes.STR,
                description="Filter by destination country (ex. ?name=Brazil)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StayViewSet(viewsets.ModelViewSet):
    queryset = (
        Stay.objects.select_related("destination")
        .prefetch_related("amenities").annotate(
            average_rating=Cast(
                Avg("stay_rating__star__value"),
                IntegerField()
            )
        )
    )
    serializer_class = StaySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the stays with filters"""
        name = self.request.query_params.get("name")
        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return StayListSerializer
        if self.action == "retrieve":
            return StayDetailSerializer
        if self.action == "upload_image":
            return StayImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific stay"""
        stay = self.get_object()
        serializer = self.get_serializer(stay, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by stay name (ex. ?name=The Plaza Hotel)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StayFramesViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = StayFrames.objects.select_related("stays")
    serializer_class = StayFramesSerializer
    permission_classes = (IsAdminUser,)


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = (
        Accommodation.objects.select_related("stay")
        .prefetch_related("amenities")
    )
    serializer_class = AccommodationSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the accommodations with filters"""
        name = self.request.query_params.get("name")
        amenities = self.request.query_params.get("amenities")
        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if amenities:
            amenities_ids = self._params_to_ints(amenities)
            queryset = queryset.filter(amenities__id__in=amenities_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AccommodationListSerializer
        if self.action == "retrieve":
            return AccommodationDetailSerializer
        if self.action == "upload_image":
            return AccommodationImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific room"""
        room = self.get_object()
        serializer = self.get_serializer(room, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "amenities",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by amenity id (ex. ?amenities=2,5)",
            ),
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by accommodation name (ex. ?name=standard)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AmenityViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = (IsAdminUser,)


class AddStarRatingDestinationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RatingDestinationCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddStarRatingStayViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RatingStayCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDestinationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReviewDestinationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewStayViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReviewStaySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return (
            Booking.objects.filter(user=user)
            .select_related("user", "stay", "rooms")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return BookingListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
