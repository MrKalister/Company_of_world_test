import requests

from config.settings import env

API_KEY = env.str('YANDEX_API_KEY')
YANDEX_WEATHER_URL = env.str(
    'YANDEX_WEATHER_URL', 'https://api.weather.yandex.ru/v2/forecast/'
)
HEADERS = {'X-Yandex-API-Key': API_KEY}


def get_weather(city):
    """Return the weather for a city from weather service."""

    params = {
        'lat': city.latitude,
        'lon': city.longitude,
    }
    response = requests.get(YANDEX_WEATHER_URL, params=params, headers=HEADERS)
    data = response.json().get('fact')
    return parse_data(data)


def parse_data(data):
    """Parse result from weather service."""

    return {
        'temperature': data.get('temp'),
        'pressure_mm': data.get('pressure_mm'),
        'wind_speed': data.get('wind_speed'),
    }
