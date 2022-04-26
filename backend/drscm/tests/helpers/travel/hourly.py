from drscm.models import HourlyTravel, Project
from faker import Faker
faker = Faker()


def create_random_hourly_travel(timestamp, project: Project = None, hours: int = 1, save = False):


    hourly_travel = HourlyTravel(timestamp=timestamp, hours=hours)

    if project:
        hourly_travel.project = project
        hourly_travel.owner = project.owner

    if save:
        hourly_travel.save()

    return hourly_travel