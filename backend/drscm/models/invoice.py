import uuid
from enum import Enum
from django.db import models
from drscm.models import Client, Project, WorkSession, FixedTravel, HourlyTravel


class TaxRegulation(Enum):

    DUTCH = 0
    EUROPEAN = 1
    NON_EUROPEAN = 2

    @classmethod
    def generate_choices(cls):
        choices = []
        for member in cls:
            choices.append((member.value, member.name))
        return choices


class Invoice(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(to="User", on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    work_sessions = models.ManyToManyField(WorkSession, blank=True)
    fixed_travels = models.ManyToManyField(FixedTravel, blank=True)
    hourly_travels = models.ManyToManyField(HourlyTravel, blank=True)
    tax_regulation = models.PositiveSmallIntegerField(
        choices=TaxRegulation.generate_choices(),
        blank=False,
        null=False,
        default=TaxRegulation.DUTCH.value,
    )

    def __str__(self):
        return f"{self.id}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.client = self.project.client
        self.owner = self.project.client.owner

        super(Invoice, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
