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


class ReviewDestinationInline(admin.TabularInline):
    model = ReviewDestination
    extra = 1
    readonly_fields = ("user", )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "country",)
    search_fields = ("name", "country")
    inlines = [ReviewDestinationInline]
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'"
        )

    get_image.short_description = "Image"


class ReviewStayInline(admin.TabularInline):
    model = ReviewStay
    extra = 1
    readonly_fields = ("user", )


class StayFramesInline(admin.TabularInline):
    model = StayFrames
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='130' height='100'"
        )

    get_image.short_description = "Stay pictures"


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "destination",)
    search_fields = ("name", "country")
    inlines = [StayFramesInline, ReviewStayInline]
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'"
        )

    get_image.short_description = "Image"


@admin.register(StayFrames)
class StayFramesAdmin(admin.ModelAdmin):
    list_display = ("title", "stays", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'"
        )

    get_image.short_description = "Image"


class AccommodationFramesInline(admin.TabularInline):
    model = AccommodationFrames
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='130' height='100'"
        )

    get_image.short_description = "Stay pictures"


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "type_room", "number_rooms", "number_beds", "get_image")
    search_fields = ("name", "type_room")
    inlines = [AccommodationFramesInline]
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='60' height='50'"
        )

    get_image.short_description = "Image"


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
    readonly_fields = ("user",)


@admin.register(ReviewStay)
class ReviewStayAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stay")
    readonly_fields = ("user",)


@admin.register(ReviewDestination)
class ReviewDestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "destination")
    readonly_fields = ("user",)


@admin.register(RatingStay)
class RatingStayAdmin(admin.ModelAdmin):
    list_display = ("stay", "star", "user")


@admin.register(RatingDestination)
class RatingDestinationAdmin(admin.ModelAdmin):
    list_display = ("destination", "star", "user")


admin.site.register(RatingStar)
admin.site.register(Amenity)
