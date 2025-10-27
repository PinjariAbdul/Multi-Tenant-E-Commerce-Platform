from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Tenant


class User(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Store Owner'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"