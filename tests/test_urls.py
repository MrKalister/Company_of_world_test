from typing import Optional

from django.test import TestCase, Client

from config.settings import SERVICE_URL
from tests.factory import CityFactory


class WeatherUrlTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class with a test record in the database and a client."""
        super().setUpClass()
        cls.client: Client = Client()
        cls.city = CityFactory(name='Москва')

    def _test_weather(self, city_name: str, expected_status: int) -> None:
        """Test the weather endpoint with a given city name."""
        response = self.client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        self.assertEqual(response.status_code, expected_status)

    def test_weather_positive(self) -> None:
        """Test the weather endpoint with a valid city name."""
        city_name = WeatherUrlTest.city.name
        self._test_weather(city_name, 200)

    def test_weather_negative(self) -> None:
        """Test the weather endpoint with an invalid city name."""
        city_name = 'Нет_такого_города'
        self._test_weather(city_name, 404)


class WeatherListUrlTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class with a client and fixtures."""
        super().setUpClass()
        cls.client: Client = Client()
        CityFactory.create_batch(15)

    def _test_cities_list(
            self, expected_status: int, data: Optional[dict] = None
    ) -> None:
        """Test the cities_list endpoint with optional parameters."""
        response = self.client.get(SERVICE_URL + 'cities_list/', data=data)
        self.assertEqual(response.status_code, expected_status)

    def test_list_without_params(self) -> None:
        """Test the cities_list endpoint without parameters."""
        self._test_cities_list(200)

    def test_list_with_params(self) -> None:
        """Test the cities_list endpoint with parameters."""
        data = {'names_only': True, 'limit': 10, 'offset': 0}
        self._test_cities_list(200, data=data)
