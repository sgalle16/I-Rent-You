from django import forms
from .models import Property, PropertyFeature, PropertyImage
from .custom_fields import MultipleFileField


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'type_of_property', 'time_for_rent', 'location', 'address', 'size',
                  'rental_price', 'status', 'description']
        labels = {
            'title': 'Titulo',
            'type_of_property': 'Tipo de Propiedad',
            'time_for_rent': 'Tiempo de Alquiler',
            'location': 'Ubicación',
            'address': 'Dirección',
            'size': 'Tamaño',
            'rental_price': 'Precio de Alquiler',
            'status': 'Disponibilidad',
            'description': 'Descripción'
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Descripción', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True


class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model = PropertyFeature
        fields = ['num_bedrooms', 'num_bathrooms',
                  'parking_spaces', 'garden', 'pool', 'furnished']
        labels = {
            'num_bedrooms': 'Número de habitaciones',
            'num_bathrooms': 'Número de baños',
            'parking_spaces': 'Parqueaderos',
            'garden': 'Jardin o Patio',
            'pool': 'Pscina',
            'furnished': 'Amueblado',
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['images', 'is_main_image']
        labels = {
            'images': 'Imágenes',
            'is_main_image': 'Imagen Principal',
        }
        widgets = {
            'is_main_image': forms.CheckboxInput(),
        }

    images = MultipleFileField()
