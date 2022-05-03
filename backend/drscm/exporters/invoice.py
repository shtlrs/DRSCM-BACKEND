import tempfile
import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseNotFound
from docx import Document

from utils.docx.mergers.invoice import InvoiceMerger
from utils.docx.table_generators import DutchBillsTableExtender
from drscm.interfaces.exporter import AbstractExporter
from drscm.proxies import InvoiceProxy
from backend.settings.dev import BASE_INVOICE_TEMPLATE


class InvoiceExporter(AbstractExporter):
    def export(self, invoice_proxy: InvoiceProxy):
        try:
            print(tempfile.gettempdir())
            temp_dir = tempfile.gettempdir()
            path = os.path.join(temp_dir, f"{invoice_proxy.id}.docx")
            output_path = os.path.join(temp_dir, f"{invoice_proxy.id}-output.docx")
            document = Document(BASE_INVOICE_TEMPLATE)
            billables_table = document.tables[1]

            if invoice_proxy.is_dutch():
                table_generator = DutchBillsTableExtender(
                    invoice_proxy=invoice_proxy, table=billables_table
                )
            elif invoice_proxy.is_european():
                table_generator = DutchBillsTableExtender(
                    invoice_proxy=invoice_proxy, table=billables_table
                )
            elif invoice_proxy.is_non_european():
                table_generator = DutchBillsTableExtender(
                    invoice_proxy=invoice_proxy, table=billables_table
                )
            else:
                table_generator = DutchBillsTableExtender(
                    invoice_proxy=invoice_proxy, table=billables_table
                )
            table_generator.generate()
            document.save(path)
            merger = InvoiceMerger(path)
            merger.merge(output_path, invoice_proxy=invoice_proxy)
            response = FileResponse(open(output_path, "rb"), filename=output_path, as_attachment=True)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                output_path
            )
        except ObjectDoesNotExist:
            response = HttpResponseNotFound(f'Invoice {invoice_proxy.id} does not exist')
        except IOError:
            response = HttpResponseNotFound('Could not generate invoice')
        return response
