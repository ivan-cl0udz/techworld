from django.db import models
from django.contrib.auth.models import User
from django.db import models
import os
from datetime import datetime
# Create your models here.





# orders/models.py

from django.db import models
from django.contrib.auth.models import User
  # only if you want to keep a relation




from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)



    def __str__(self):
        return f"{self.full_name or 'Unnamed'}, {self.city or ''}"


class Order(models.Model):
    session_key = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    # Snapshot of shipping info
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.pk or ''} - {self.full_name or 'No Name'}"
