from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

from user.serializers import UserSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({"token": token})
        return Response({"error": "Invalid credentials"}, status=400)
