from abc import abstractmethod
from django.db.models import Model
from .meta_classes import AbstractModelMeta


class Billable(Model, metaclass=AbstractModelMeta):
    @abstractmethod
    def get_total(self):
        """
        Returns the total amount of the billable
        """

    class Meta:
        abstract = True
