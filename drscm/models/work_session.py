import uuid
from django.db import models
from utils.date import get_current_timestamp_with_null_seconds, timestamp_to_date_string
from .project import Project


class WorkSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_timestamp = models.IntegerField(editable=True, null=False, blank=False)
    end_timestamp = models.IntegerField(editable=True, null=False, blank=False)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        to="User", related_name="work_sessions", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("start_timestamp",)

    @classmethod
    def create(cls):
        """
        Creates a new Work Session
        """
        work_session = cls(start_timestamp=get_current_timestamp_with_null_seconds())
        return work_session

    def end(self):
        """
        Ends the worksession at the current time
        """
        self.end_timestamp = get_current_timestamp_with_null_seconds()
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.owner = self.project.owner

        if self.start_timestamp > self.end_timestamp:
            raise ValueError(
                f"Start time: {timestamp_to_date_string(self.start_timestamp)} should be"
                f" before end time: {timestamp_to_date_string(self.end_timestamp)}"
            )

        super(WorkSession, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        return f"Session: {self.start_timestamp} -> {self.end_timestamp}"
