import uuid
from django.db import models
from backend.utils.date import get_timestamp_with_null_seconds


class WorkSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_timestamp = models.IntegerField(editable=True)
    end_timestamp = models.IntegerField(editable=True)


    @classmethod
    def create(cls):
        work_session = cls(start_timestamp=get_timestamp_with_null_seconds())
        return work_session

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.end_timestamp = get_timestamp_with_null_seconds()
        super(WorkSession, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)