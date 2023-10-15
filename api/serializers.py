from rest_framework import serializers

from city.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'latitude',
            'longitude',
        )


class WeatherSerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    pressure_mm = serializers.IntegerField()
    wind_speed = serializers.FloatField()
