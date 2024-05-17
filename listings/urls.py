from django.urls import path
from .views import home, get_listings_for_map, submit_property, PropertyDetailView, get_cities

app_name = "listings_app"

urlpatterns = [
    path("", home, name="home"),
    path("<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("get_listings/", get_listings_for_map, name="get_listings"),
    path("submit_property/", submit_property, name="submit_property"),
    path("submit_property/get_cities/", get_cities, name="get_cities"),
]
