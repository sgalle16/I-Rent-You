from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartamento'),
        ('house', 'Casa'),
        ('room', 'Habitación'),
        ('office', 'Oficina'),
        ('studio', 'Aparta-Estudio'),
    ]

    type_of_property = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    time_for_rent = models.PositiveIntegerField(help_text="Time for rent in months")
    location = models.CharField(max_length=100)
    size = models.PositiveIntegerField(help_text="Size in square meters")
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    images = models.ImageField(
        upload_to='media/property/property_images/', blank=True, null=True)

    # The line `owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')` in
    # the `Property` model is creating a foreign key relationship between the `Property` model and the
    # `User` model.
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='properties')
    description = models.TextField(blank=True)

    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_of_property} en {self.location} Disponible: {self.availability}"



# The `PropertyFeature` class represents the features of a property, including the number of bedrooms
# and bathrooms, parking spaces, and whether it has a garden or pool.
class PropertyFeature(models.Model):
    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name='features')
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField()
    garden = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    backyard =  models.BooleanField(default=False)
    def __str__(self):
        return f"Características de {self.property.description}: {self.num_bedrooms} Beds | {self.num_bathrooms} Baths"


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
