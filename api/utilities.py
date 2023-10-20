import time
from typing import Dict, Any, Union

import requests

from city.models import City
from config.settings import PLUG, env

API_KEY = env.str('YANDEX_API_KEY')
YANDEX_WEATHER_URL = env.str(
    'YANDEX_WEATHER_URL', 'https://api.weather.yandex.ru/v2/forecast/'
)
HEADERS = {'X-Yandex-API-Key': API_KEY}
CACHE_EXPIRY = 1800  # 30 minutes
weather_cache = {}

if PLUG:
    CACHE_EXPIRY = 0
test_data = {'temp': 12, 'pressure_mm': 764, 'wind_speed': 2.8}


def get_weather(city: City) -> Dict[str, Union[str, int]]:
    """Return the weather for a city from the weather service with caching."""

    # Check if weather data for this city is in the cache and not expired
    if city in weather_cache:
        cached_data: Dict[str, Union[str, int]] = weather_cache[city][0]
        timestamp: float = weather_cache[city][1]
        current_time: float = time.time()

        # If the data is still fresh, return it
        if current_time - timestamp <= CACHE_EXPIRY:
            return cached_data

    params: Dict[str, Union[str, float]] = {
        'lat': city.latitude,
        'lon': city.longitude,
    }

    data: Dict[str, Union[str, int]] = (
        (
            requests.get(YANDEX_WEATHER_URL, params=params, headers=HEADERS)
            .json()
            .get('fact')
        )
        if not PLUG
        else test_data
    )

    # Parse the data and store it in the cache with the current timestamp
    weather_data: Dict[str, Union[str, int]] = parse_data(data)
    weather_cache[city] = (weather_data, time.time())

    return weather_data


def parse_data(data: Dict[str, Any]) -> Dict[str, Union[str, int]]:
    """Parse the result from the weather service."""
    keys_to_extract = ['temp', 'pressure_mm', 'wind_speed']
    return {key: data.get(key) for key in keys_to_extract}
