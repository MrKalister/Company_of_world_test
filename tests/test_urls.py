from django.test import TestCase, Client

from city.models import City
from config.settings import env

SERVICE_URL = env.str('SERVICE_URL', 'http://127.0.0.1:8000/api/v1/')


class StaticURLTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.city = City.objects.create(
            name='Москва',
            latitude='55.755787',
            longitude='37.617634',
        )

    # Positive cases
    def test_weather_status_positive(self):
        city_name = self.city.name
        response = self.guest_client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        self.assertEqual(response.status_code, 200)

    def test_weather_result_positive(self):
        city_name = self.city.name
        exp_data = ['temperature', 'pressure_mm', 'wind_speed']
        response = self.guest_client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        for el in exp_data:
            self.assertIn(el, response.data)

    # Negative cases
    def test_weather_status_negative(self):
        city_name = 'Нет_такого_города'

        response = self.guest_client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        self.assertEqual(response.status_code, 404)

    def test_weather_result_negative(self):
        city_name = 'Нет_такого_города'
        exp_err = f'City with name {city_name} does not exist'

        response = self.guest_client.get(
            SERVICE_URL + 'weather/', data={'city': city_name}
        )
        self.assertEqual(response.data.get('error'), exp_err)
