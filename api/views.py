import logging

from rest_framework import status as s
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from api.serializers import CitySerializer, WeatherSerializer
from api.uttilities import get_weather
from city.models import City

logger = logging.getLogger('django.server')


class WeatherView(RetrieveAPIView):
    """Return info about select city."""

    queryset = City.objects.all()
    serializer_class = WeatherSerializer

    def retrieve(self, request, *args, **kwargs):
        msg, status, response = None, None, None
        # Get city_name from request and reformat to
        city_name = request.GET.get('city', '').capitalize()
        # Get object
        city = get_object_or_404(City, name=city_name)

        try:
            # serializing result
            response = self.get_serializer(get_weather(city)).data
        except (AttributeError, KeyError) as error:
            msg = f'{type(error).__name__} - {str(error)}'
            status = s.HTTP_400_BAD_REQUEST
        except Exception as error:
            msg = f'Unknown error: {type(error).__name__} - {str(error)}'
            status = s.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            if msg and status:
                logger.error(msg, exc_info=True)
                return Response({'error': msg}, status=status)
            return Response(response)


class SitiesView(ListAPIView):
    """Return list of cities, which exist in DB."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
