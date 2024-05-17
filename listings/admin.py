from django.contrib import admin
from .models import Listing, Region, City, Image

admin.site.register(Region)
admin.site.register(City)
admin.site.register(Image)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    raw_id_fields = ["city", "owner"]

