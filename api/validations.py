""" This module contains functions to check
if given parameters are correct """

from datetime import datetime


def check_measurement_units(units):
    """
    Checks if the given units are supported
    Supported units: metric, imperial
    :param units: name of the given measurement units
    :return: True if the data is correct or False if not
    """
    if units not in ('metric', 'imperial'):
        return False
    return True

def check_time_period(period):
    """
    Checks if the given time period is correct
    First date should not be greater than the second one
    :param period: time period
    :return: True if the data is correct or False if not
    """
    if period[0] > period[1]:
        return False
    return True


def check_datetime_format(date_time):
    """
    Checks if the datetime format is correct
    Correct datetime format: YYYY-MM-DDTHH:MM:SS
    :param date_time: given datetime
    :return: True if the data is correct or False if not
    """
    try:
        datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return False
    return True
