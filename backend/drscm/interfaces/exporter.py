from abc import ABC, abstractmethod

from django.http import HttpResponse

from .billable import Billable


class AbstractExporter(ABC):
    @abstractmethod
    def export(self, billable: Billable) -> HttpResponse:
        """
        Exports the provided billable and sends it over to the client over HTTP
        """
