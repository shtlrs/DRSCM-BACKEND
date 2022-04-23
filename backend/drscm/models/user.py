import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import UUIDField


class User(AbstractUser):

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = UserManager()