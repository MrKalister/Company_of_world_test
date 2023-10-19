import factory

from city.models import City


class CityFactory(factory.django.DjangoModelFactory):
    """Generate random cities."""

    class Meta:
        model = City

    name = factory.Faker('city')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
