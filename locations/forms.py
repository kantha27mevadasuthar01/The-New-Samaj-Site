from django import forms
from .models import MandirLocation

class LocationForm(forms.ModelForm):
    class Meta:
        model = MandirLocation
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location Name'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Address', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Description', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country'}),
            'google_maps_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Google Maps Link'}),
        }
        labels = {
            'google_maps_link': 'Google Maps URL',
            'name': 'Temple/Location Name',
            'description': 'About this Location',
        }
