import os
from typing import Any, Dict, List
from unittest.mock import patch

from django.test import TestCase

from api.utilities import get_weather, test_data
from city.models import City
from tests.factory import CityFactory


class GetWeatherUtilTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class with a test record in the database."""
        super().setUpClass()
        cls.city: City = CityFactory(name='Тестовый город')

    def test_answer_from_util(self) -> None:
        """Test if get_weather returns expected data."""
        city: City = GetWeatherUtilTest.city
        response: Dict[str, Any] = get_weather(city)

        with patch.dict(os.environ, {'PLUG': 'True'}):
            self.assertDictEqual(response, test_data)

    def test_content_from_get_weather(self) -> None:
        """Test if get_weather response contains expected keys."""
        city = GetWeatherUtilTest.city
        response: Dict[str, Any] = get_weather(city)
        exp_data: List[str] = ['temp', 'pressure_mm', 'wind_speed']
        for el in exp_data:
            self.assertIn(el, response)

    def test_exception(self) -> None:
        """Test if get_weather raises AttributeError with invalid input."""
        self.assertRaises(AttributeError, get_weather, city='')
