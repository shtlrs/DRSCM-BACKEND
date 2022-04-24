from faker import Faker
from drscm.models import Project

fake = Faker()


def create_random_project(
    name=fake.name(),
    hourly_rate=fake.pyfloat(positive=True, max_value=175, right_digits=1),
    travel_hourly_rate=fake.pyfloat(positive=True, max_value=175, right_digits=1),
    travel_fixed_rate=fake.pyfloat(positive=True, max_value=175, right_digits=1),
    currency=fake.currency_code(),
):

    return Project(
        name=name,
        hourly_rate=hourly_rate,
        travel_hourly_rate=travel_hourly_rate,
        travel_fixed_rate=travel_fixed_rate,
        currency=currency,
    )
