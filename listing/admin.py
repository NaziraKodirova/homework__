from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Listing, Region, City, Image, Country, Address

admin.site.register(Image)
@admin.site.register(Address)
@admin.site.register(City) 
@admin.site.register(Region)
@admin.site.register(Country)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    raw_id_fields = ["country", "city", "owner"]

