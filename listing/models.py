from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Country(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, models.CASCADE, related_name="region_city")
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Address(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

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
        
    class PriceType(models.TextChoices):
        s = "$", "$"
        sum ="Sum", "Sum"

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    about = models.TextField()
    l_type = models.CharField(max_length=2, choices=Type.choices, default=Type.APARTMENT)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.RENT)
    number_of_rooms = models.PositiveIntegerField()
    price = models.FloatField()
    price_type = models.CharField(max_length=10, choices=PriceType.choices, default=PriceType.sum)
    owner = models.ForeignKey(get_user_model(), models.CASCADE, related_name="user_listing")
    area = models.CharField(max_length=255)
    city = models.ForeignKey(City, models.CASCADE, related_name="city_listing")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_listing")
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("listing_app:property_detail", args=[str(self.pk)])


class Image(models.Model):
    image = models.ImageField(upload_to="photos/")
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="listing_images")

    def __str__(self):
        return self.image.name[:-5]
