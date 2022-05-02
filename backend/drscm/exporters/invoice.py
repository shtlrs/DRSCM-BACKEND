from django.core.exceptions import ObjectDoesNotExist
from docx import Document

from drscm.docx_table_generators import DutchBillsTableGenerator
from drscm.interfaces.exporter import AbstractExporter
from drscm.proxies import InvoiceProxy
from backend.settings.dev import BASE_INVOICE_TEMPLATE


class InvoiceExporter(AbstractExporter):
    def export(self, invoice: InvoiceProxy):
        try:
            invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
            document = Document(BASE_INVOICE_TEMPLATE)
            billables_table = document.tables[1]

            if invoice_proxy.is_dutch():
                table_generator = DutchBillsTableGenerator(invoice_proxy=invoice_proxy, table=billables_table)
            elif invoice_proxy.is_european():
                table_generator = DutchBillsTableGenerator(invoice_proxy=invoice_proxy, table=billables_table)
            elif invoice_proxy.is_non_european():
                table_generator = DutchBillsTableGenerator(invoice_proxy=invoice_proxy, table=billables_table)
            else:
                table_generator = DutchBillsTableGenerator(invoice_proxy=invoice_proxy, table=billables_table)
            table_generator.generate()
            document.save(f"{invoice_proxy.id}.docx")
        except ObjectDoesNotExist:
            pass
