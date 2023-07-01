from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import LoginSerializer


User = get_user_model()

SIGNUP_URL = reverse("user:signup")
LOGIN_URL = reverse("user:login")
MANAGE_URL = reverse("user:manage")


class UserSignUpViewTestCase(APITestCase):

    def setUp(self):
        User.objects.all().delete()

    def test_user_signup(self):

        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "username": "TestUser",
            "phone_number": "+123456789"
        }

        response = self.client.post(SIGNUP_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")


class UserLoginViewTestCase(APITestCase):

    def test_user_login_invalid_credentials(self):

        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }

        response = self.client.post(LOGIN_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("non_field_errors", response.data)


class LoginSerializerTestCase(APITestCase):

    def test_validate_invalid_credentials(self):

        serializer = LoginSerializer(data={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        self.assertFalse(serializer.is_valid())

        errors = serializer.errors

        self.assertIn("non_field_errors", errors)
        self.assertEqual(errors["non_field_errors"][0], "Invalid credentials")


class ManageUserViewTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@example.com",
            password=make_password("testpassword")
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_retrieve_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.get(MANAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        data = {
            "email": "newemail@example.com",
            "password": "newpassword",
            "username": "NewUser",
            "phone_number": "987654321"
        }

        response = self.client.put(MANAGE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email="newemail@example.com")

        self.assertEqual(user.email, "newemail@example.com")
