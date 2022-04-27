import uuid
from django.db import models


class Travel(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False
    )

    timestamp = models.IntegerField(null=False, unique=True, blank=False)

    rate = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

