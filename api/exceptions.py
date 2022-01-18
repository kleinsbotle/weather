from rest_framework.exceptions import APIException


class WeatherAPIException(APIException):
    """
    Custom APIException to give detailed information in case of API exceptions
    :param detail: information message
    :param status_code: returned HTTP status code
    """

    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code
