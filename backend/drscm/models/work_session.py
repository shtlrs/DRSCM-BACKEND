import uuid
from django.contrib.auth.models import User
from django.db import models
from utils.date import get_timestamp_with_null_seconds
from .project import Project

class WorkSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_timestamp = models.IntegerField(editable=True)
    end_timestamp = models.IntegerField(editable=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(to='User', related_name='work_sessions', on_delete=models.CASCADE)

    @classmethod
    def create(cls):
        work_session = cls(start_timestamp=get_timestamp_with_null_seconds())
        return work_session

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.end_timestamp = get_timestamp_with_null_seconds()
        super(WorkSession, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
