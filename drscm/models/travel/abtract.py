import uuid
from django.db import models


class Travel(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False
    )

    timestamp = models.IntegerField(null=False, unique=True, blank=False)

    rate = models.FloatField(null=True, blank=True)

    extra_costs = models.FloatField(null=False, blank=False, default=0)

    class Meta:
        abstract = True
