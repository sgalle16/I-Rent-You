from django.contrib import admin

from .models import Property, PropertyComment, PropertyFeature, PropertyRating, User

admin.site.register(Property)
admin.site.register(PropertyComment)
admin.site.register(PropertyRating)
admin.site.register(User)
admin.site.register(PropertyFeature)