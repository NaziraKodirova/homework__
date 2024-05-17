from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, models.CASCADE, related_name="region_city")
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Listing(models.Model):

    class Type(models.TextChoices):
        HOUSE = "HS", "House"
        APARTMENT = "AP", "Apartment"

    class Status(models.TextChoices):
        SALE = "SL", "Sale"
        RENT = "RN", "Rent"
        DONE = "DN", "Done"

    address = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    about = models.TextField()
    l_type = models.CharField(max_length=2, choices=Type.choices, default=Type.APARTMENT)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.RENT)
    number_of_rooms = models.PositiveIntegerField()
    price = models.CharField(max_length=500)
    owner = models.ForeignKey(get_user_model(), models.CASCADE, related_name="user_listing")
    area = models.CharField(max_length=255)
    city = models.ForeignKey(City, models.CASCADE, related_name="city_listing")

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("listings_app:property_detail", args=[str(self.pk)])


class Image(models.Model):
    image = models.ImageField(upload_to="photos/")
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="listings_images")

    def __str__(self):
        return self.image.name[:-5]
