from django.db import models
import uuid


class Client(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    owner = models.ForeignKey(to="User", related_name="clients", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
