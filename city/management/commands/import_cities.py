import os

import openpyxl
from django.core.management.base import BaseCommand

from city.models import City
from config.settings import DATA_FILES_DIR


class Command(BaseCommand):
    """Uploader data in the database from a excel file."""

    def handle(self, *args, **options):
        file_name = 'spisok_gorodov_RU.xlsx'
        file_path = os.path.join(DATA_FILES_DIR, file_name)

        try:
            sheet = openpyxl.load_workbook(file_path).active
            cities_to_create = []
            existing_city_names = set(
                City.objects.values_list('name', flat=True)
            )

            for row in sheet.iter_rows(min_row=1, values_only=True):
                name, latitude, longitude = row[0], row[1], row[2]
                if name not in existing_city_names:
                    cities_to_create.append(
                        City(
                            name=name,
                            latitude=latitude,
                            longitude=longitude,
                        )
                    )

            if cities_to_create:
                City.objects.bulk_create(cities_to_create)
                self.stdout.write(
                    self.style.SUCCESS('Data uploaded successfully.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No new cities to upload.')
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found.'))
