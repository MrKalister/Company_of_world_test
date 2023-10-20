from rest_framework import serializers

from city.models import City


class CitySerializer(serializers.ModelSerializer):
    """Serialize all information about a city."""

    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'latitude',
            'longitude',
        )


class CityListSerializer(serializers.ModelSerializer):
    """Serialize only names of cities."""

    class Meta:
        model = City
        fields = ('name',)


class WeatherSerializer(serializers.Serializer):
    """Serialize weather in a city."""

    city_name = serializers.CharField()
    temp = serializers.IntegerField()
    pressure_mm = serializers.IntegerField()
    wind_speed = serializers.FloatField()
