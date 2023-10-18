from django.test import TestCase

from city.models import City


class CityModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Help to avoid error:
        # 'AttributeError: type object '<имя_класса>' has no attribute 'cls_atomics'
        super().setUpClass()
        # Creating a test record in the database
        # and save the created record as a class variable
        cls.city = City.objects.create(
            name='Москва',
            latitude='55.755787',
            longitude='37.617634',
        )

    def test_verbose_name(self):
        """Verbose_name in the fields matches the expected."""

        city = CityModelTest.city
        field_verboses = {
            'name': 'Название',
            'latitude': 'Широта',
            'longitude': 'Долгота',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    city._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_name_is_name_fild(self):
        """__str__ city is a str with content city.name."""

        city = CityModelTest.city
        expected_object_name = city.name
        self.assertEqual(expected_object_name, str(city))
