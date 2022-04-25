from faker import Faker
from drscm.models import WorkSession, Project
from utils.date import date_time_to_timestamp

fake = Faker()


def create_random_work_session(start_time_stamp: int = None, end_time_stamp: int = None, project: Project = None) -> WorkSession:
    start_time_stamp = date_time_to_timestamp(start_time_stamp) or None
    end_time_stamp = date_time_to_timestamp(end_time_stamp) or None
    work_session = WorkSession(start_time_stamp=start_time_stamp, end_time_stamp=end_time_stamp)
    if project:
        work_session.project = project
        work_session.owner = project.owner

    return work_session
