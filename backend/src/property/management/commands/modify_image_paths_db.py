from django.core.management.base import BaseCommand
from property.models import Property
import json


class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        items = Property.objects.all()
        for item in items:
            item.images.name = f"media/property/property_images/{item.title}.jpg"
            # item.images.name = f"{item.images.name[0:13]}{item.title}.jpg"
            item.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated with the illustrations of the movies'))
        
