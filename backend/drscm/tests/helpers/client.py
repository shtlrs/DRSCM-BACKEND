from faker import Faker
from drscm.models import Client

fake = Faker()


def create_random_client(
    name=None,
    country=None,
    postal_code=None,
    city=None,
    street=None,
    owner=None,
    save=False,
):
    name = name or fake.name()
    country = country or fake.country()
    postal_code = postal_code or fake.postcode()
    city = city or fake.city()
    street = street or fake.street_name()

    client = Client(
        name=name, country=country, postal_code=postal_code, city=city, street=street
    )

    if owner:
        client.owner = owner

    if save:
        client.save()

    return client
