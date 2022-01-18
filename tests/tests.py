from django.test import TestCase

from api.validations import check_measurement_units, check_datetime_format, \
    check_time_period


class TestCheckUnits(TestCase):

    def setUp(self):
        self.check_units = check_measurement_units

    def test_metric(self):
        self.assertEqual(self.check_units('metric'), True)

    def test_imperial(self):
        self.assertEqual(self.check_units('imperial'), True)

    def test_incorrect(self):
        self.assertEqual(self.check_units('meters'), False)


class TestCheckDateTime(TestCase):

    def setUp(self):
        self.check_datetime = check_datetime_format

    def test_correct_datetime(self):
        dt = '2022-01-01T00:00:00'
        self.assertEqual(self.check_datetime(dt), True)

    def test_incorrect_date(self):
        dt = '2022-35-01T00:00:00'
        self.assertEqual(self.check_datetime(dt), False)

    def test_incorrect_time(self):
        dt = '2022-01-01T163:00:00'
        self.assertEqual(self.check_datetime(dt), False)

    def test_incorrect_format(self):
        dt = '2022/01/01T10:00:00'
        self.assertEqual(self.check_datetime(dt), False)


class CheckTimePeriod(TestCase):

    def setUp(self):
        self.check_period = check_time_period

    def test_start_smaller_end(self):
        start = '2022-01-01T12:00:00'
        end = '2022-01-10T00:00:00'
        self.assertEqual(self.check_period([start, end]), True)

    def test_start_bigger_end(self):
        start = '2022-01-10T00:00:00'
        end = '2022-01-01T12:00:00'
        self.assertEqual(self.check_period([start, end]), False)

    def test_start_eq_end(self):
        datetime = '2022-05-05T15:00:00'
        self.assertEqual(self.check_period([datetime, datetime]), True)
