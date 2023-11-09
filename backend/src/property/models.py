from django.db import models
from django.contrib.auth.models import AbstractUser
from Users.models import User


PROPERTY_TYPES = [
    ('apartment', 'Apartamento'),
    ('house', 'Casa'),
    ('room', 'Habitación'),
    ('office', 'Oficina'),
    ('studio', 'Aparta-Estudio'),
]

TIME_RENT = [
    ('1', '1 mes'),
    ('3', '3 meses'),
    ('6', '6 meses'),
    ('12', '1 año'),
    ('24', '2 años'),
    ('36', '3 años'),
]

STATUS_CHOICES = [
    ('rented', 'Alquilado'),
    ('available', 'Disponible'),
    ('pending', 'Pendiente'),
    ('other', 'Otro'),
]

NUM_BEDROOM = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

NUM_BATHROOM = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class Property(models.Model):

    title = models.CharField(max_length=100)
    type_of_property = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    time_for_rent = models.CharField(max_length=20,
                                     choices=TIME_RENT,  help_text="Tiempo de renta en meses")
    location = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=300, blank=False)
    size = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Tamaño en metros cuadrados (m²)")
    rental_price = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Precio de Alquiler (COP)")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # The line `owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')` in
    # the `Property` model is creating a foreign key relationship between the `Property` model and the
    # `User` model.
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='properties', null=True)
    description = models.TextField(blank=True)

    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_of_property} | {self.title} en {self.location} - Estado: {self.get_status_display()}"

    def get_main_image(self):
        # Obtener la imagen principal de la propiedad
        try:
            return self.images.get(is_main_image=True)
        except PropertyImage.DoesNotExist:
            # Si no hay una imagen principal, devolver la primera imagen
            try:
                return self.images.first()
            except PropertyImage.DoesNotExist:
                return None


# The `PropertyFeature` class represents the features of a property, including the number of bedrooms
# and bathrooms, parking spaces, and whether it has a garden or pool.
class PropertyFeature(models.Model):
    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name='features')
    num_bedrooms = models.CharField(max_length=10,
                                    choices=NUM_BEDROOM, unique=False)
    num_bathrooms = models.CharField(max_length=10,
                                     choices=NUM_BATHROOM, unique=False)
    parking_spaces = models.PositiveIntegerField()
    garden = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    backyard = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)

    def __str__(self):
        return f"Características de {self.property.title}: {self.num_bedrooms} Beds | {self.num_bathrooms} Baths"


# The `PropertyImage` class represents an image associated with a property.
class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(
        upload_to='media/property/property_images/', blank=True, null=True)
    is_main_image = models.BooleanField(
        default=False, null=True, blank=True, help_text="¿Es la imagen principal de tu propiedad?")

    def __str__(self):
        return self.property.title


# The `PropertyComment` class represents a comment made by a user on a property, with fields for the
# property, user, content, and time created.
class PropertyComment(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# The `PropertyRating` class represents a rating given by a user to a property, with a value between 1
# and 5.
class PropertyRating(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    value = models.PositiveIntegerField(choices=RATING_CHOICES)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
        # return f"Calificación de {self.user.username} para {self.property.get_type_of_property_display()} en {self.property.location}"
