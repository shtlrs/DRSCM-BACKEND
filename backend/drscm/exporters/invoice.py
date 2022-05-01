from django.core.exceptions import ObjectDoesNotExist

from drscm.interfaces.exporter import AbstractExporter
from drscm.interfaces.billable import Billable
from drscm.proxies import InvoiceProxy
from docx import Document
from backend.settings.dev import BASE_INVOICE_TEMPLATE


class InvoiceExporter(AbstractExporter):

    def export(self, invoice: Billable, template_path: str):
        try:
            invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
            document = Document(BASE_INVOICE_TEMPLATE)
            # First thing to check is the tax regulations
            # We'd need to make some kind of a generator per TAX regulation
            if invoice_proxy.fixed_travels.exists():
                # Add fixed travel row here
                pass
            if invoice_proxy.hourly_travels_proxy.exists():
                # Add fixed travel row here
                pass

            # add total rows here with styling




        except ObjectDoesNotExist:
            # To be defined later
            pass


