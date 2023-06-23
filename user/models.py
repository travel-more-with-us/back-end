from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PHONE_NUMBER_MAX_LENGTH = 15

    STATUS_CHOICES = (
        'Tenant',
        'Landlord',
    )

    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH)
    residency = models.CharField(max_length=63)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='tenant')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
