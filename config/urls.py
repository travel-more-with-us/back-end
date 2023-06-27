from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("TravelMore.urls")),
    path("user/", include("user.urls", namespace="user")),
    path("admin/", admin.site.urls),
]
