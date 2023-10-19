from typing import Any

from django.test import TestCase, Client

from city.models import City
from config.settings import SERVICE_URL


class WeatherViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class with a client."""
        super().setUpClass()
        cls.client: Client = Client()

    def test_get_lastcity(self) -> None:
        """Test getting the last city when two cities have the same name."""

        city_name: str = 'Moscow'
        City.objects.create(
            name=city_name, latitude=55.700000, longitude=37.6000000
        )
        city2: City = City.objects.create(
            name=city_name, latitude=55.7111111, longitude=37.6111111
        )
        obj: City = City.objects.filter(name=city_name).order_by('id').last()
        response: Any = self.client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )

        self.assertEqual(obj.id, city2.id)
        self.assertEqual(response.status_code, 200)
