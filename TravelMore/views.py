from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from TravelMore.models import Destination, Stay
from TravelMore.serializers import DestinationSerializer, StaySerializer, BookingSerializer


@api_view(['GET'])
def homepage(request):
    destinations = Destination.objects.all()
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def destination_page(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    stays = Stay.objects.filter(destination=destination)
    serializer = StaySerializer(stays, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_booking(request, stay_id):
    try:
        stay = Stay.objects.get(id=stay_id)
    except Stay.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(stay=stay)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
