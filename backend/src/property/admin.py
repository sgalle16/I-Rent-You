from django.contrib import admin

from .models import Property, PropertyComment, PropertyRating, User

admin.site.register(Property)
admin.site.register(PropertyComment)
admin.site.register(PropertyRating)
admin.site.register(User)