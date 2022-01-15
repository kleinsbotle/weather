from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timestamp = models.PositiveBigIntegerField()
    temp = models.FloatField()
    description = models.CharField(max_length=30)

    def __str__(self):
        return f'Weather forecast for {self.city} at {self.timestamp}'
