from celery import shared_task
from celery.utils.log import get_task_logger

from api.services import WeatherReportService


logger = get_task_logger(__name__)


@shared_task(bind=True)
def collect_forecast_data(self):
    WeatherReportService.collecting_weather_data()
