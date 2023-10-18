from django.test import TestCase

from city.models import City


class CityModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Creating a test record in the database
        # and save the created record as a class variable
        cls.city = City.objects.create(
            name='Москва',
            latitude='55.755787',
            longitude='37.617634',
        )

    def test_name_label(self):
        """Verbose_name of the name field matches the expected one."""

        city = CityModelTest.city
        # Get the verbose_name value for name from the City class property
        verbose = city._meta.get_field('name').verbose_name
        self.assertEqual(verbose, 'Название')

    def test_latitude_label(self):
        """Verbose_name of the latitude field matches the expected one."""

        city = CityModelTest.city
        # Get the verbose_name value for latitude from the City class property
        verbose = city._meta.get_field('latitude').verbose_name
        self.assertEqual(verbose, 'Широта')

    def test_longitude_label(self):
        """Verbose_name of the longitude field matches the expected one."""

        city = CityModelTest.city
        # Get the verbose_name value for longitude from the City class property
        verbose = city._meta.get_field('longitude').verbose_name
        self.assertEqual(verbose, 'Долгота')

    def test_object_name_is_name_fild(self):
        """__str__ city is a str with content city.name."""

        city = CityModelTest.city
        expected_object_name = city.name
        self.assertEqual(expected_object_name, str(city))
