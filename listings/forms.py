from django import forms
from .models import Listing, Region, City


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
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Select Regions")
    image_field = MultipleFileField()

    class Meta:
        model = Listing
        fields = ["region", "city", "address", "lat", "long", "about", "l_type", "status", "number_of_rooms", "price", "owner",
                  "area"]

