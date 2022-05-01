from faker import Faker
from drscm.models import User

fake = Faker()


def create_random_user(
    username=None, email=None, password=None, is_superuser=False, save=False
) -> User:
    username = username if username else fake.name()
    email = email if email else fake.email()
    password = password if password else fake.password()

    if is_superuser:
        user = User.objects.create_superuser(
            username=username, email=email, password=password
        )
    else:
        user = User.objects.create_user(username=username, email=email, password=password)

    user.raw_password = password

    if save:
        user.save()

    return user
