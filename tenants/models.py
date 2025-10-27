from django.db import models


class Tenant(models.Model):
    store_name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()

    def __str__(self):
        return self.store_name
