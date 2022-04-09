from django.db import models
import uuid


class WorkSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start = models.IntegerField(editable=True)
    end = models.IntegerField(editable=True)
