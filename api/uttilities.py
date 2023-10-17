import time

import requests

from config.settings import env

API_KEY = env.str('YANDEX_API_KEY')
PLUG = env.bool('PLUG', False)  # Заглушка
YANDEX_WEATHER_URL = env.str(
    'YANDEX_WEATHER_URL', 'https://api.weather.yandex.ru/v2/forecast/'
)
HEADERS = {'X-Yandex-API-Key': API_KEY}
CACHE_EXPIRY = 1800  # 30 minutes
weather_cache = {}


def get_weather(city):
    """Return the weather for a city from the weather service with caching."""

    # Check if weather data for this city is in the cache and not expired
    if city in weather_cache:
        cached_data, timestamp = weather_cache[city]
        current_time = time.time()

        # If the data is still fresh, return it
        if current_time - timestamp <= CACHE_EXPIRY:
            return cached_data

    params = {
        'lat': city.latitude,
        'lon': city.longitude,
    }
    if PLUG:
        data = {'temp': 12, 'pressure_mm': 764, 'wind_speed': 2.8}
    else:
        response = requests.get(
            YANDEX_WEATHER_URL, params=params, headers=HEADERS
        )
        data = response.json().get('fact')

    # Parse the data and store it in the cache with the current timestamp
    weather_data = parse_data(data)
    weather_cache[city] = (weather_data, time.time())

    return weather_data


def parse_data(data):
    """Parse the result from the weather service."""

    return {
        'temperature': data.get('temp'),
        'pressure_mm': data.get('pressure_mm'),
        'wind_speed': data.get('wind_speed'),
    }
