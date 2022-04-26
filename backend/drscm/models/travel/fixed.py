from django.db import models
from drscm.models import Project
from .abtract import Travel


class FixedTravel(Travel):

    occurrences = models.IntegerField(null=False, blank=False)
    owner = models.ForeignKey(to="User", related_name="fixed_travels", on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, related_name="fixed_travels", on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.owner = self.project.owner
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)