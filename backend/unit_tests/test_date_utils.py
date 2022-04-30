from utils.date import purify_timestamp
from datetime import datetime
from django.test import TestCase


class DateUtilsTests(TestCase):
    def test_purify_timestamp(self):
        timestamp = datetime(
            year=2022, month=3, day=20, hour=15, minute=50, second=37, microsecond=0
        ).timestamp()
        timestamp = purify_timestamp(timestamp)
        self.assertEqual(timestamp, 1647787800.0)
