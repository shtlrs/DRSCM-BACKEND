from abc import ABC, abstractmethod
from .billable import Billable


class AbstractExporter(ABC):

    @abstractmethod
    def export(self, billable: Billable, template_path: str):
        pass
