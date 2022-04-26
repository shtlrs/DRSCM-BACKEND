from django.db import models
from drscm.models import Project
from .abtract import Travel


class HourlyTravel(Travel):

    hours = models.FloatField(null=False, blank=False)
    owner = models.ForeignKey(
        to="User",
        related_name="hourly_travels",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    project = models.ForeignKey(
        to=Project,
        related_name="hourly_travels",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.owner = self.project.owner
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
