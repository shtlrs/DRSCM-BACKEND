from faker import Faker
from drscm.models import Client

fake = Faker()


def create_random_client(
    name=fake.name(),
    country=fake.country(),
    postal_code=fake.postcode(),
    city=fake.city(),
    street=fake.street_name(),
    owner=None,
    save=False,
):
    client = Client(
        name=name, country=country, postal_code=postal_code, city=city, street=street
    )

    if owner:
        client.owner = owner

    if save:
        client.save()

    return client
