from datetime import timedelta
from faker import Faker
from drscm.models import WorkSession, Project
from utils.date import date_time_to_timestamp


fake = Faker()


def create_random_work_session(
    start_time_stamp: int = None,
    end_time_stamp: int = None,
    project: Project = None,
    save=False,
) -> WorkSession:
    end_time_stamp = end_time_stamp or fake.future_datetime()
    start_time_stamp = start_time_stamp or fake.date_time_between_dates(
        datetime_end=end_time_stamp + timedelta(minutes=-20)
    )
    end_time_stamp = date_time_to_timestamp(end_time_stamp)
    start_time_stamp = date_time_to_timestamp(start_time_stamp)
    work_session = WorkSession(
        start_timestamp=start_time_stamp, end_timestamp=end_time_stamp
    )
    if project:
        work_session.project = project
        work_session.owner = project.owner

    if save:
        work_session.save()

    return work_session
