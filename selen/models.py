from __future__ import unicode_literals

from django.db import models

# Create your models here.


# main category links
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
    done = models.BooleanField(default=False)


class TripAdvisorHotelInfo(models.Model):
    hotel = models.ForeignKey(TripAdvisorHotel)
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    image_url = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    done = models.BooleanField(default=False)
    postal = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
