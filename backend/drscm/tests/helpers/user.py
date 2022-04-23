from faker import Faker
from drscm.models import User

fake = Faker()


def create_random_user(username=fake.name(), email=fake.email(), password=fake.password()):

    user = User(username=username, email=email)

    user.set_password(password)

    return user
