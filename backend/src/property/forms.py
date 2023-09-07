from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['type_of_property', 'time_for_rent', 'location', 'size',
                  'rental_price', 'availability', 'images', 'owner', 'description']
