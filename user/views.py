from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from user.models import User
from user.serializers import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({'token': token})
        return Response({'error': 'Invalid credentials'}, status=400)
