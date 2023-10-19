import logging

from rest_framework import status as s
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from api.serializers import (
    CitySerializer,
    WeatherSerializer,
    CityListSerializer,
)
from api.utilities import get_weather
from city.models import City
from config.settings import PLUG

logger = logging.getLogger('django.server')


class WeatherView(RetrieveAPIView):
    """Return info about select city."""

    queryset = City.objects.all()
    serializer_class = WeatherSerializer
    # From setting - DEFAULT_THROTTLE_RATES
    throttle_scope = 'low_request' if not PLUG else 'anon'

    def retrieve(self, request, *args, **kwargs):
        # Get city_name from request and reformat it
        city_name = request.GET.get('city', '').capitalize()
        try:
            # Get object
            city = get_object_or_404(City, name=city_name)
        except City.MultipleObjectsReturned:
            # There may be more than one city with the same name in the DB.
            # Return only the first city by id
            city = (
                self.get_queryset()
                .filter(name=city_name)
                .order_by('id')
                .last()
            )
        try:
            response = self.get_serializer(get_weather(city)).data
        except Exception as error:
            msg = f'{type(error).__name__} - {str(error)}'
            logger.error(msg, exc_info=True)
            return Response(
                {'error': msg}, status=s.HTTP_500_INTERNAL_SERVER_ERROR
            )
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
