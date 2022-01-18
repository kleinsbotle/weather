import csv

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.models import User, Forecast
from api.services import WeatherForecastService
from api import serializers
from api.exceptions import WeatherAPIException
from api.validations import check_datetime_format, check_time_period


# Time of page caching in seconds
CACHE_TIME = 60


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ForecastView(generics.RetrieveAPIView):
    """
    Gets 5 day weather forecast within 3-hour step for the chosen city
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TIME))
    def get(self, request, city, units):
        """
        GET controller
        :param request:
        :param city: name of the city
        :param units: unit of temperature measurement.
        metric is for Fahrenheit
        imperial is for Celsius
        :return: requested 5 day weather forecast information
        """

        res = WeatherForecastService.get_weather_forecast(city, units)
        return Response(data=res, status=res['status'])


class ReportView(APIView):
    """
    Downloads collected weather data for certain time period as .csv file
    """
    permission_classes = [IsAuthenticated]

    serializer_class = serializers.ForecastSerializer

    def get_serializer(self, queryset, many=True):
        """ Get serializer for Forecast object """
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, start, end):
        """
        GET controller
        :param request:
        :param start: start of the period. Example: 2022-01-17T17:00:00
        :param end: end of the period.
        :return:
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="forecast_report.csv"'
        time_period = [start, end]
        for time in time_period:
            if not check_datetime_format(time):
                raise WeatherAPIException('Incorrect datetime format.'
                                          'The correct format is '
                                          'YYYY-MM-DDTHH:MM:SS',
                                          status.HTTP_400_BAD_REQUEST)
        if not check_time_period(time_period):
            raise WeatherAPIException('Incorrect time period. '
                                      'Start date should be '
                                      'smaller than end date',
                                      status.HTTP_400_BAD_REQUEST)
        queryset = Forecast.objects.filter(dt__range=time_period)
        if not queryset.exists():
            raise WeatherAPIException('There is no forecast data'
                                      ' for given period of time',
                                      status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(
            queryset,
            many=True
        )
        header = serializers.ForecastSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
