from faker import Faker
from drscm.models import Project, Client

fake = Faker()


def create_random_project(
    name=None,
    hourly_rate=None,
    travel_hourly_rate=None,
    travel_fixed_rate=None,
    currency=None,
    client: Client = None,
    save=False,
):
    name = name or fake.name()
    hourly_rate = hourly_rate or fake.pyfloat(positive=True, max_value=175, right_digits=1)
    travel_hourly_rate = travel_hourly_rate or fake.pyfloat(
        positive=True, max_value=175, right_digits=1
    )
    travel_fixed_rate = travel_fixed_rate or fake.pyfloat(
        positive=True, max_value=175, right_digits=1
    )
    currency = currency or fake.currency_code()

    project = Project(
        name=name,
        hourly_rate=hourly_rate,
        travel_hourly_rate=travel_hourly_rate,
        travel_fixed_rate=travel_fixed_rate,
        currency=currency,
    )

    if client:
        project.client = client
        project.owner = client.owner

    if save:
        project.save()

    return project
