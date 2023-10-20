from django.core.management.base import BaseCommand
from property.models import Property
import json
import os
import numpy as np


class Command(BaseCommand):
    help = 'Load propertys from property_descriptions.json into the property model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        # Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        # El path del archivo property_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        # json_file_path = '../properties_descriptions.json'
        json_file_path = '/home/shaan/I-Rent-You/properties_complete.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            properties = json.load(file)

        # Add products to the database
        cont = 0
        for property in properties:
            # Se asegura que la película no exista en la base de datos
            exist = Property.objects.filter(title=property['title']).first()
            if not exist:
                cont += 1
                Property.objects.create(title=property['title'], description=property['description'])

        self.stdout.write(self.style.SUCCESS(
            f'Successfully added {cont} products to the database'))
