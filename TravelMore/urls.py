from django.urls import path, include
from rest_framework import routers

from TravelMore.views import (
    DestinationViewSet,
    StayViewSet,
    StayFramesViewSet,
    AccommodationViewSet,
    AddStarRatingDestinationViewSet,
    AddStarRatingStayViewSet,
    ReviewDestinationViewSet,
    ReviewStayViewSet,
    AmenityViewSet,
    BookingViewSet,
)

app_name = "TravelMore"

router = routers.DefaultRouter()
router.register(
    "destinations",
    DestinationViewSet,
    basename="destinations"
)
router.register(
    "stays", StayViewSet, basename="stays"
)
router.register(
    "accommodations",
    AccommodationViewSet,
    basename="accommodations"
)
router.register(
    "amenities", AmenityViewSet, basename="amenities"
)
router.register(
    "stay-frames", StayFramesViewSet, basename="stay-frames"
)
router.register(
    "rating-destinations",
    AddStarRatingDestinationViewSet,
    basename="rating-destinations",
)
router.register(
    "rating-stays",
    AddStarRatingStayViewSet,
    basename="rating-stays",
)
router.register(
    "review-destinations",
    ReviewDestinationViewSet,
    basename="review-destinations"
)
router.register(
    "review-stays", ReviewStayViewSet, basename="review-stays"
)
router.register(
    "bookings", BookingViewSet, basename="bookings"
)


urlpatterns = [path("", include(router.urls))]
