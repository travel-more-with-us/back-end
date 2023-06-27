from django.urls import path

from TravelMore import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('destination/<int:destination_id>/', views.destination_page, name='destination_page'),
    path('stay/<int:stay_id>/booking/', views.create_booking, name='create_booking'),
]
