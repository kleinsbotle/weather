from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import User, Weather
from .service import WeatherAPIService
from . import serializers


CACHE_TIME = 60


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ForecastView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TIME))
    def get(self, request, city, units):
        res = WeatherAPIService.get_weather_forecast(city, units)
        if res['success']:
            return Response(data=res, status=res['status'])
        return Response(data=res, status=res['status'])


class ReportView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Weather.objects.all()
    serializer_class = serializers.WeatherSerializer
