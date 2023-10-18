import logging

from rest_framework import status as s
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response

from api.serializers import (
    CitySerializer,
    WeatherSerializer,
    CityListSerializer,
)
from api.uttilities import get_weather
from city.models import City

logger = logging.getLogger('django.server')


class WeatherView(RetrieveAPIView):
    """Return info about select city."""

    queryset = City.objects.all()
    serializer_class = WeatherSerializer

    throttle_scope = 'low_request'  # setting - DEFAULT_THROTTLE_RATES

    def retrieve(self, request, *args, **kwargs):
        msg, status, response = None, s.HTTP_400_BAD_REQUEST, None
        # Get city_name from request and reformat it
        city_name = request.GET.get('city', '').capitalize()

        try:
            # Get object
            city = City.objects.get(name=city_name)
            # serializing result
            response = self.get_serializer(get_weather(city)).data
        except (AttributeError, KeyError) as error:
            msg = f'{type(error).__name__} - {str(error)}'
        except City.DoesNotExist:
            msg = f'City with name {city_name} does not exist'
            status = s.HTTP_404_NOT_FOUND
        except City.MultipleObjectsReturned:
            # There may be more than one city with the same name in the DB.
            # Return only the first city by id
            city = City.objects.filter(name=city_name).first()
            response = self.get_serializer(get_weather(city)).data
        except Exception as error:
            msg = f'Unknown error: {type(error).__name__} - {str(error)}'
            status = s.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            if msg:
                logger.error(msg, exc_info=True)
                return Response({'error': msg}, status=status)
            return Response(response)


class SitiesView(ListAPIView):
    """Return list of cities."""

    serializer_class = CitySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.names_only = False

    def get_queryset(self):
        # Check if the request wants only city names
        self.names_only = self.request.query_params.get('names_only', False)
        if self.names_only:
            return City.objects.values('name')
        return City.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.names_only:
            return CityListSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
