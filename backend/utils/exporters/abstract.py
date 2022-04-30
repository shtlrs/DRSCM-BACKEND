from abc import ABC, abstractmethod
from django.db.models import Model


class AbstractExporter(ABC):
    @abstractmethod
    def export(self, model: Model):
        ...
