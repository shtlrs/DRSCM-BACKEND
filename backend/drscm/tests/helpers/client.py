from faker import Faker
from drscm.models import Client

fake = Faker()


def create_fake_client(name=fake.name(), country=fake.country(), postal_code=fake.postcode(),
                       city=fake.city(), street=fake.street_name()):

    return Client(name=name,
                  country=country,
                  postal_code=postal_code,
                  city=city,
                  street=street)