from django import forms
from .models import Property, PropertyFeature


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['type_of_property', 'time_for_rent', 'location', 'size',
                  'rental_price', 'availability', 'images', 'owner', 'description']

class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model = PropertyFeature
        fields = ['num_bedrooms', 'num_bathrooms', 'parking_spaces', 'garden', 'pool']