# Generated by Django 4.1.3 on 2023-10-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('city', '0002_alter_city_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.FloatField(verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.FloatField(verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
    ]
