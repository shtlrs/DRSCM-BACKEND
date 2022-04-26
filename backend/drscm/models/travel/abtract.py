from django.db import models


class Travel(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, null=False, blank=False)
    timestamp = models.IntegerField(null=False, unique=True, blank=False)

    class Meta:
        abstract = True

