from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, LoginSerializer


class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response({"token": token}, status=status.HTTP_200_OK)
