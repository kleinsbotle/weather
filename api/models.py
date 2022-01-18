from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class City(models.Model):
    """
    Model represents different cities
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Forecast(models.Model):
    """
    Model represents weather forecast for a certain city
    Forecast information contains:
    :field dt: datetime of forecast
    :field temp: temperature
    :field description: weather description
    """
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    temp = models.FloatField()
    description = models.CharField(max_length=30)

    def __str__(self):
        return f'Forecast for {self.city_id.name} on {self.dt}'
