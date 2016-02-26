from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TripAdvisorHotelCity(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    done = models.BooleanField(default=False)


class TripAdvisorHotel(models.Model):
    category = models.ForeignKey(TripAdvisorHotelCity)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
