from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from datetime import datetime
from time import sleep
from .cities import cities
import requests

API_KEY = '2fb9aec1bb16dc9cf07583e27ddecc2f'
API = "http://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}"


class WeatherAPIService:

    @staticmethod
    def get_weather_forecast(city, units):
        try:
            url = API.format(
                city=city,
                units=units,
                api_key=API_KEY)
            response = requests.get(url)

            data = response.json()['list']

            data_list = []
            for item in data:
                data_dict = {}
                date_time = datetime.utcfromtimestamp(int(item['dt'])).strftime('%Y-%m-%d %H:%M:%S')
                data_dict['timestamp'] = date_time
                data_dict['temp'] = item['main']['temp']
                data_dict['description'] = item['weather'][0]['description']
                data_list.append(data_dict)
            return {
                'success': True,
                "msg": "success",
                "data": data_list,
                "status": status.HTTP_200_OK}
        except Exception as e:
            return {
                'success': False,
                "data": None,
                "msg": f'Error {str(e)}',
                "status": status.HTTP_400_BAD_REQUEST}


class WeatherReportService:

    @staticmethod
    def collecting_weather_data():
        while True:
            for city in cities:
                try:
                    url = API.format(
                        city=city,
                        units='metric',
                        api_key=API_KEY)
                    response = requests.get(url)
                except Exception as e:
                    pass
            sleep(3600)