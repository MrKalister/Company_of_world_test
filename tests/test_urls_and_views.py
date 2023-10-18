from django.test import TestCase, Client

from city.models import City
from config.settings import env

SERVICE_URL = env.str('SERVICE_URL', 'http://127.0.0.1:8000/api/v1/')


class WeatherViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Help to avoid error:
        # 'AttributeError: type object '<имя_класса>' has no attribute 'cls_atomics'
        super().setUpClass()
        cls.guest_client = Client()
        # Creating a test record in the database
        # and save the created record as a class variable
        cls.city = City.objects.create(
            name='Москва',
            latitude='55.755787',
            longitude='37.617634',
        )

    def _test_weather(self, city_name, expected_status, expected_data):
        response = self.guest_client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        self.assertEqual(response.status_code, expected_status)

        if expected_data:
            if isinstance(expected_data, list):
                for el in expected_data:
                    self.assertIn(el, response.data)
            elif isinstance(expected_data, dict):
                for key, value in expected_data.items():
                    self.assertEqual(response.data.get(key), value)

    def test_weather_positive(self):
        city_name = WeatherViewTest.city.name
        exp_data = ['temperature', 'pressure_mm', 'wind_speed']
        self._test_weather(city_name, 200, exp_data)

    def test_weather_negative(self):
        city_name = 'Нет_такого_города'
        exp_data = {'error': f'City with name {city_name} does not exist'}
        self._test_weather(city_name, 404, exp_data)
