from django.db.utils import IntegrityError
from django.test import TestCase

from city.models import City
from tests.factory import CityFactory


class CityModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class by creating a City instance."""
        super().setUpClass()
        cls.city: City = CityFactory()

    def test_field_verbose_names(self) -> None:
        """Field verbose names match expected values."""
        city: City = CityModelTest.city
        field_verboses: dict[str, str] = {
            'name': 'Название',
            'latitude': 'Широта',
            'longitude': 'Долгота',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    city._meta.get_field(field).verbose_name, expected_value
                )

    def test_str_method(self) -> None:
        """Test '__str__' method of City model."""
        city: City = CityModelTest.city
        expected_object_name: str = city.name
        self.assertEqual(expected_object_name, str(city))

    def test_duplicate_name_validation(self) -> None:
        """Test duplicate name validation."""
        city2: City = CityFactory(name=CityModelTest.city.name)
        self.assertIsInstance(city2, City)
        self.assertEqual(City.objects.filter(name=city2.name).count(), 2)

    def test_coordinates_integrity(self) -> None:
        """Test coordinates integrity (IntegrityError)."""
        with self.assertRaises(IntegrityError):
            CityFactory(
                name=CityModelTest.city.name,
                latitude=CityModelTest.city.latitude,
                longitude=CityModelTest.city.longitude,
            )
