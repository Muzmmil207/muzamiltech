from django.db import models


class GuestLocation(models.Model):
    ip_address = models.CharField(max_length=255)
    city = models.CharField(max_length=75)
    region = models.CharField(max_length=75)
    latitude = models.CharField(max_length=75)
    longitude = models.CharField(max_length=75)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.region

    class Meta:
        abstract = True
