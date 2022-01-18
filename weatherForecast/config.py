"""
This file contains secret keys
In production it should be added to .gitignore
"""

API_URL = "http://api.openweathermap.org/" \
          "data/2.5/forecast?q={city}&units={units}&appid={api_key}"

OPEN_WEATHER_API_KEY = '2fb9aec1bb16dc9cf07583e27ddecc2f'

DJANGO_SECRET_KEY = \
    'django-insecure-%b5o472eqm6+dy3k(muwu(+v-408w68aq1123)gmc@jb8$f*-q'
