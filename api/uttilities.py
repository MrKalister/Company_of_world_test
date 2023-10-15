import requests

from config.settings import env

API_KEY = env.str('YANDEX_API_KEY')
URL = f'https://api.weather.yandex.ru/v2/forecast/'
HEADERS = {'X-Yandex-API-Key': API_KEY}


def get_weather(city):
    """Returns the weather from a city."""

    params = {
        'lat': city.latitude,
        'lon': city.longitude,
    }
    response = requests.get(URL, params=params, headers=HEADERS)
    data = response.json().get('fact')
    return {
        'temperature': data.get('temp'),
        'pressure_mm': data.get('pressure_mm'),
        'wind_speed': data.get('wind_speed'),
    }
