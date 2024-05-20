from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import DetailView, FormView
from .models import Listing, Image, City
from .forms import ListingForm


def home(request):
    listings = Listing.objects.all()
    houses = Listing.objects.all()
    city = ""
    status = ""
    if request.GET.get("city") is not None:
        city = request.GET.get("city")
    if request.GET.get("status") is not None:
        status = request.GET.get("status")
    if city:
        houses = houses.filter(city__name=city)
    return render(request, "index.html", context={"listings": listings, "houses": houses})


def navbar(request):
    return render(request, "navbar.html")


class PropertyDetailView(DetailView):
    model = Listing
    template_name = "property.html"


def submit_property(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("region", None)
            listing_instance = form.save(commit=False)
            listing_instance.save()
            images = request.FILES.getlist('image_field')
            for image in images:
                Image.objects.create(listing=listing_instance, image=image)
            return redirect("listing_app:property_detail", pk=str(listing_instance.id))
        else:
            print(form.errors)
    listing_form = ListingForm
    return render(request, "submit-property.html", context={"listing_form": listing_form})


def get_cities(request):
    region_id = request.GET.get('region_id')
    cities = City.objects.filter(region_id=region_id).values('id', 'name', 'lat', 'long')
    return JsonResponse(list(cities), safe=False)


def get_listings_for_map(request):
    listings = Listing.objects.all()  # You can filter listings if needed
    listing_data = []
    for listing in listings:
        urls = [img.image.url for img in listing.listing_images.all()]
        carousel = "<div id='carousel-container'>"
        for url in urls:
            carousel += f"<div class='carousel-item'><img class='carousel-image' src='{ url }' alt=''></div>\n"
        carousel += "</div>"
        listing_data.append({
            'address': listing.address,
            'lat': listing.lat,
            'lng': listing.long,
            'about': listing.about,
            'rooms': listing.number_of_rooms,
            'price': listing.price,
            'owner': listing.owner.username,
            'city': listing.city.name,
            'region': listing.city.region.name,
            'country': listing.country.name,
            'urls': listing.get_absolute_url(),
            'images': carousel,
            # Add other relevant data for markers
        })
    return JsonResponse(listing_data, safe=False)  # Don't escape here
