from django.db import models


class City(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        db_index=True,
    )
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'latitude', 'longitude'],
                name='unique_city',
            )
        ]

    def __str__(self):
        return self.name
