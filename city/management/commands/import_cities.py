import os
from typing import Set, List

import openpyxl
from django.core.management.base import BaseCommand

from city.models import City
from config.settings import DATA_FILES_DIR, FILE_NAME


class Command(BaseCommand):
    """Uploader data in the database from an Excel file."""

    def handle(self, *args, **options) -> None:
        file_path: str = os.path.join(DATA_FILES_DIR, FILE_NAME)

        try:
            sheet = openpyxl.load_workbook(file_path).active
            cities_to_create: List[City] = []
            existing_city_names: Set = set(
                City.objects.values_list('name', flat=True)
            )

            for row in sheet.iter_rows(min_row=1, values_only=True):
                name: str = row[0].title()
                latitude: float = row[1]
                longitude: float = row[2]
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
