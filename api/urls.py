from django.urls import path

from api.views import SitiesView, WeatherView

urlpatterns = [
    path('weather/', WeatherView.as_view()),
    path('cities_list/', SitiesView.as_view()),
]
