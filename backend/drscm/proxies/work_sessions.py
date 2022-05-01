from drscm.models import WorkSession
from utils.date import timestamp_to_date_string, seconds_to_hours, time_stamp_to_date_time


class WorkSessionProxy(WorkSession):


    class Meta:
        proxy = True

    def get_date(self):
        date_string = timestamp_to_date_string(self.start_timestamp)
        return date_string

    def get_session_duration(self):
        end = time_stamp_to_date_time(self.end_timestamp)
        start = time_stamp_to_date_time(self.start_timestamp)
        difference = end - start
        return seconds_to_hours(difference.seconds)

    def get_total(self):
        return self.project.hourly_rate * self.get_session_duration()
