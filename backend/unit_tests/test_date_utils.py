from utils.date import (
    purify_timestamp,
    seconds_to_hours,
    get_current_timestamp_with_null_seconds,
    date_time_to_timestamp,
    timestamp_to_date_string,
    time_stamp_to_date_time,
)
from datetime import datetime, timezone
from django.test import TestCase


class DateUtilsTests(TestCase):
    def test_purify_timestamp(self):
        self.skipTest(
            "Currently there's an issue with the timezone when launched on github machines"
        )
        timestamp = datetime(
            year=2022,
            month=3,
            day=20,
            hour=15,
            minute=50,
            second=37,
            microsecond=0,
            tzinfo=timezone.utc,
        ).timestamp()
        timestamp = purify_timestamp(timestamp)
        self.assertEqual(timestamp, 1647787800.0)

    def test_date_time_to_timestamp(self):
        date = datetime(
            year=2022,
            month=3,
            day=20,
            hour=15,
            minute=50,
            second=37,
            microsecond=0,
            tzinfo=timezone.utc,
        )
        timestamp = date_time_to_timestamp(date)
        self.assertEqual(1647791400.0, timestamp)

    def test_time_stamp_to_date_time(self):
        timestamp = 1647791437.0
        target_date = datetime(
            year=2022,
            month=3,
            day=20,
            hour=15,
            minute=50,
            second=37,
            microsecond=0,
            tzinfo=timezone.utc,
        )
        date = time_stamp_to_date_time(timestamp)
        self.assertEqual(target_date, date)

    def test_timestamp_to_date_string(self):
        timestamp = datetime(
            year=2022,
            month=3,
            day=20,
            hour=15,
            minute=50,
            second=37,
            microsecond=0,
            tzinfo=timezone.utc,
        ).timestamp()
        date_string = timestamp_to_date_string(timestamp)
        self.assertEqual("2022-03-20", date_string)

    def test_get_current_timestamp_with_null_seconds(self):
        now = datetime.now().replace(second=0, microsecond=0)
        timestamp = get_current_timestamp_with_null_seconds()
        self.assertEqual(now.timestamp(), timestamp)

    def test_seconds_to_hours(self):
        # 1 hours
        seconds = 3600
        hours = seconds_to_hours(seconds)
        self.assertEqual(1, hours)
        # 30 minutes
        seconds = 1800
        hours = seconds_to_hours(seconds)
        self.assertEqual(0.5, hours)
        # 45 minutes
        seconds = 2700
        hours = seconds_to_hours(seconds)
        self.assertEqual(0.75, hours)
        # 1 second
        seconds = 1
        hours = seconds_to_hours(seconds)
        self.assertEqual(0, hours)
        # 47 minutes and 30 seconds
        seconds = 2850
        hours = seconds_to_hours(seconds)
        self.assertEqual(0.8, hours)
