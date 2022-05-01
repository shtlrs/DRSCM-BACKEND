from drscm.interfaces.exporter import AbstractExporter
from drscm.interfaces.billable import Billable


class InvoiceExporter(AbstractExporter):


    def export(self, invoice: Billable, template_path: str):
        pass