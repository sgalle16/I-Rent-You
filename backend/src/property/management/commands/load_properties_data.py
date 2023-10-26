from django.core.management.base import BaseCommand
from property.models import Property, PropertyFeature
import json
import os

class Command(BaseCommand):
    help = 'Load properties from properties_complete.json into the property model and feautures'

    def handle(self, *args, **kwargs):
        # Load properties from JSON file
        with open('/home/shaan/I-Rent-You/properties_complete.json', 'r') as file:
            properties_data = json.load(file)

        # Initialize a counter for added properties
        count = 0

        # Loop through each property in the JSON data
        for property_data in properties_data:
            # Check if the property already exists based on the title
            existing_property = Property.objects.filter(
                title=property_data['title']).first()

            if existing_property is None:
                # Property doesn't exist, create a new one
                new_property = Property(
                    title=property_data['title'],
                    description=property_data['description'],
                    images=f'media/property/property_images/{property_data["title"]}.jpg',
                    type_of_property=property_data['type_of_property'],
                    time_for_rent=property_data['time_for_rent'],
                    location=property_data['location'],
                    address=property_data['address'],
                    size=property_data['size'],
                    rental_price=property_data['rental_price'],
                    status=property_data['status']
                )
                new_property.save()

                # Create an instance of PropertyFeature associated with the new Property
                property_feature_data = property_data.get('property_feature')
                if property_feature_data:
                    property_feature = PropertyFeature(
                        property=new_property,
                        num_bedrooms=property_feature_data.get('num_bedrooms'),
                        num_bathrooms=property_feature_data.get('num_bathrooms'),
                        parking_spaces=property_feature_data.get('parking_spaces'),
                        garden=property_feature_data.get('garden'),
                        pool=property_feature_data.get('pool'),
                        backyard=property_feature_data.get('backyard'),
                        furnished=property_feature_data.get('furnished')
                    )
                    property_feature.save()

                count += 1
            else:
                # Property already exists, you can choose to update its information if needed
                pass

        self.stdout.write(self.style.SUCCESS(
            f'Successfully added {count} properties and features to the database'))