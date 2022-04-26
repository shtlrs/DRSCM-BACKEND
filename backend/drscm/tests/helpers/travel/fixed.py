from drscm.models import FixedTravel, Project
from faker import Faker

faker = Faker()


def create_random_fixed_travel(timestamp, project: Project = None, occurrences: int = 1, save=False):
    fixed_travel = FixedTravel(timestamp=timestamp, occurrences=occurrences)

    if project:
        fixed_travel.project = project
        fixed_travel.owner = project.owner

    if save:
        fixed_travel.save()

    return fixed_travel
