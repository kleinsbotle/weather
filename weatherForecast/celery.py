from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program., broker='redis://redis:6379/0'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weatherForecast.settings')

app = Celery('weatherForecast')

app.config_from_object(settings, namespace='CELERY')


# Collect forecast data every 3 hours
app.conf.beat_schedule = {
    'collect forecast data': {
        'task': 'api.tasks.collect_forecast_data',
        'schedule': crontab(),
    }
}

# Load task modules from all registered Django apps.minute=0, hour='*/3'
app.autodiscover_tasks()


@app.task(bind=True)
def create(self):
    print(f'Request {self.request!r}')
