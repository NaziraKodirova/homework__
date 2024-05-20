from django import forms
from .models import Listing, Country, City


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ListingForm(forms.ModelForm):

    lat = forms.FloatField(widget=forms.HiddenInput)
    long = forms.FloatField(widget=forms.HiddenInput)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country")
    image_field = MultipleFileField()

    class Meta:
        model = Listing
        fields = [
            "country", "city", "address", "lat", "long", "about", "l_type", "status", 
            "number_of_rooms", "price", "price_type", "owner", "area"
        ]

