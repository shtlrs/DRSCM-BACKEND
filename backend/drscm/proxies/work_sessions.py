from drscm.models import WorkSession
from datetime import timedelta
from drscm.interfaces.billable import Billable
from utils.date import (
    timestamp_to_date_string,
    seconds_to_hours,
    time_stamp_to_date_time,
    seconds_to_hours_and_minutes,
    purify_timestamp,
)


class WorkSessionProxy(WorkSession, Billable):

    start_date_string: str
    end_date_string: str
    session_duration_in_seconds: float
    session_duration: timedelta

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(WorkSessionProxy, self).__init__(*args, **kwargs)
        self.start_date_string = timestamp_to_date_string(self.start_timestamp, "%H:%M")
        self.end_date_string = timestamp_to_date_string(self.end_timestamp, "%H:%M")
        pure_start_timestamp = purify_timestamp(self.start_timestamp)
        pure_end_timestamp = purify_timestamp(self.end_timestamp)
        self.session_duration = time_stamp_to_date_time(
            pure_end_timestamp
        ) - time_stamp_to_date_time(pure_start_timestamp)

    def get_date_string(self):
        date_string = timestamp_to_date_string(self.start_timestamp)
        return date_string

    def get_session_duration_date_string(self):
        hours, minutes = seconds_to_hours_and_minutes(self.session_duration.seconds)
        return f"{hours:02}:{minutes:02}"

    def get_session_duration_in_hours(self):
        return seconds_to_hours(self.session_duration.seconds)

    def get_total(self):
        return self.project.hourly_rate * self.get_session_duration_in_hours()
