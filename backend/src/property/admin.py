from django.contrib import admin

# Register your models here.

from .models import Property, PropertyComment, PropertyRating

admin.site.register(Property)
