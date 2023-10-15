from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'latitude',
        'longitude',
    )
    list_filter = search_fields = ('name',)

    # Переопределение verbose_name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model._meta.verbose_name = 'Город'
        self.model._meta.verbose_name_plural = 'Города'


AdminSite.empty_value_display = '-empty-'
