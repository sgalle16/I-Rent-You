from django.contrib import admin

from .models import (Property, PropertyComment,
                     PropertyFeature, PropertyRating, User, PropertyImage)


class PropertyFeatureInline(admin.StackedInline):
    model = PropertyFeature


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyFeatureInline, PropertyImageInline]
    list_display = ['title', 'type_of_property', 'location', 'status']


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyComment)
admin.site.register(PropertyRating)
admin.site.register(User)
admin.site.register(PropertyFeature)
admin.site.register(PropertyImage)