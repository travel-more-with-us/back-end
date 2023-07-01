from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@example.com",
            password="testpassword",
            username="TestUser",
            phone_number="+123456789",
            residency="Some Residency",
            status="tenant"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "TestUser")
        self.assertEqual(self.user.phone_number, "+123456789")
        self.assertEqual(self.user.residency, "Some Residency")
        self.assertEqual(self.user.status, "tenant")

    def test_user_str(self):
        user = self.user

        self.assertEqual(str(user), f"{user.email}")

    def test_user_full_name(self):
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.assertEqual(self.user.full_name, "John Doe")
