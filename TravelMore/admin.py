from django.contrib import admin
from django.utils.safestring import mark_safe

from TravelMore.models import (
    Destination,
    Stay,
    StayFrames,
    Accommodation,
    AccommodationFrames,
    RatingStar,
    ReviewStay,
    ReviewDestination,
    Amenity,
    RatingStay,
    RatingDestination,
    Booking,
)


class ImageAdminMixin:
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'>"
        )

    get_image.short_description = "Image"


class PictureAdminMixin:
    readonly_fields = ("get_picture",)

    def get_picture(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='130' height='100'"
        )

    get_picture.short_description = "Extra pictures"


class ReviewDestinationInline(admin.TabularInline):
    model = ReviewDestination
    extra = 1
    readonly_fields = ("user", )


@admin.register(Destination)
class DestinationAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "country",)
    search_fields = ("name", "country")
    inlines = [ReviewDestinationInline]


class ReviewStayInline(admin.TabularInline):
    model = ReviewStay
    extra = 1
    readonly_fields = ("user", )


class StayFramesInline(PictureAdminMixin, admin.TabularInline):
    model = StayFrames
    extra = 1


@admin.register(Stay)
class StayAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "address", "destination",)
    search_fields = ("name", "country")
    inlines = [StayFramesInline, ReviewStayInline]


@admin.register(StayFrames)
class StayFramesAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("title", "stays", "get_image")


class AccommodationFramesInline(PictureAdminMixin, admin.TabularInline):
    model = AccommodationFrames
    extra = 1


@admin.register(Accommodation)
class AccommodationAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "type_room", "number_rooms", "number_beds", "get_image")
    search_fields = ("name", "type_room")
    inlines = [AccommodationFramesInline]


@admin.register(AccommodationFrames)
class AccommodationFramesAdmin(admin.ModelAdmin):
    list_display = ("title", "rooms", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'"
        )

    get_image.short_description = "Image"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "stay",
        "arrival_date",
        "departure_date",
        "number_of_guests",
        "night_price",
        "total_price"
    )


@admin.register(ReviewStay)
class ReviewStayAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stay")


@admin.register(ReviewDestination)
class ReviewDestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "destination")


@admin.register(RatingStay)
class RatingStayAdmin(admin.ModelAdmin):
    list_display = ("stay", "star", "user")


@admin.register(RatingDestination)
class RatingDestinationAdmin(admin.ModelAdmin):
    list_display = ("destination", "star", "user")


admin.site.register(RatingStar)
admin.site.register(Amenity)
