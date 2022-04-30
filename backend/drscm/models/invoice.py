import uuid
from django.db import models
from drscm.models import Client, Project, WorkSession, FixedTravel, HourlyTravel


class Invoice(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(to="User", on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    work_sessions = models.ManyToManyField(WorkSession, blank=True)
    fixed_travels = models.ManyToManyField(FixedTravel, blank=True)
    hourly_travels = models.ManyToManyField(HourlyTravel, blank=True)

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

