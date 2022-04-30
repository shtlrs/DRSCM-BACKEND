from abc import abstractmethod
from django.db.models import Model
from .meta_classes import AbstractModelMeta


class Billable(Model, metaclass=AbstractModelMeta):
    @abstractmethod
    def get_total(self):
        pass

    class Meta:
        abstract = True
