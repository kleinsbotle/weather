import requests
from datetime import datetime

from rest_framework import status

from api.cities import cities
from api.models import City, Forecast
from api.validations import check_measurement_units
from api.exceptions import WeatherAPIException
from weatherForecast.config import OPEN_WEATHER_API_KEY, API_URL


def process_forecast(forecast):
    """
    Gets timestamp, temperature and description from forecast data
    :param forecast:
    :return:
    """
    processed_forecast = {
        'dt': datetime.fromtimestamp(forecast['dt']),
        'temp': forecast['main']['temp'],
        'description': forecast['weather'][0]['description']
    }
    return processed_forecast


class WeatherForecastService:
    """
    Service interacts with Open Weather API
    Gets datetime, temperature and weather description for given city
    from Open Weather API response
    """

    @staticmethod
    def get_weather_forecast(city, units):
        if not check_measurement_units(units):
            raise WeatherAPIException('Incorrect units of measurement. '
                                      'Use imperial for Fahrenheit '
                                      'and metric for Celsius.',
                                      status.HTTP_400_BAD_REQUEST)
        url = API_URL.format(
            city=city,
            units=units,
            api_key=OPEN_WEATHER_API_KEY)
        try:
            response = requests.get(url)
        except ConnectionError:
            raise WeatherAPIException('Could not connect to the OpenWeather',
                                      status.HTTP_502_BAD_GATEWAY)
        try:
            forecasts = response.json()['list']
            processed_forecasts = []
            for forecast in forecasts:
                processed_forecasts.append(process_forecast(forecast))
        except KeyError:
            return {
                'success': False,
                'msg': 'Unable to get forecast. '
                       'OpenWeather did not send '
                       'the required information.',
                'data': None,
                'status': status.HTTP_200_OK}
        return {
            'success': True,
            'msg': "success",
            'data': processed_forecasts,
            'status': status.HTTP_200_OK}


class WeatherReportService:
    """
    Service interacts with Open Weather API
    Collects weather forecast data for nearest time for the list of 100 cities
    Saves collected weather report in database
    """

    @staticmethod
    def collecting_weather_data():
        for city in cities:
            url = API_URL.format(
                city=city,
                units='metric',
                api_key=OPEN_WEATHER_API_KEY)
            try:
                response = requests.get(url)
            except ConnectionError:
                print('Unable to connect to OpenWeather')
                return None

            city_record, created = City.objects.get_or_create(name=city)
            try:
                # Gets info for the nearest timestamp
                forecast = response.json()['list'][0]
                processed_forecast = process_forecast(forecast)
            except KeyError:
                print(f'Unable to create report. OpenWeather did not '
                      f'send the required information for {city}.')
                return None
            obj = Forecast(city_id=city_record, **processed_forecast)
            obj.save()
