from typing import List
from drscm.interfaces.merger import DocumentMerger
from drscm.proxies import InvoiceProxy
from utils.date import timestamp_to_date_string
from mailmerge import MailMerge


class InvoiceMerger(DocumentMerger):

    def prep_data_for_merge(self, invoice_proxy: InvoiceProxy) -> dict:
        data = {
            "client_name": f"{invoice_proxy.client.name}",
            "fao": f"{invoice_proxy.client.name}",
            "address": f"{invoice_proxy.client.street}",
            "postal_code": f"{invoice_proxy.client.postal_code}",
            "city": f"{invoice_proxy.client.city}",
            "country": f"{invoice_proxy.client.country}",
            "purchase_order": "TEST PO",
            "invoice_number": "TEST INVOICE NUMBER",
            "hourly_rate": f"{invoice_proxy.project.hourly_rate}",
        }
        return data

    def prep_table_data_for_merge(self, invoice_proxy: InvoiceProxy) -> List[dict]:
        work_session_data = [
            {
                "date": timestamp_to_date_string(work_session.start_timestamp),
                "start": work_session.start_date_string,
                "stop": work_session.end_date_string,
                "cumulated_hours": work_session.get_session_duration_date_string(),
            }
            for work_session in invoice_proxy.work_sessions_proxy
        ]

        return work_session_data

    def merge(self, output_file_path, **kwargs):
        invoice_proxy = kwargs.get("invoice_proxy")
        field_data = self.prep_data_for_merge(invoice_proxy=invoice_proxy)
        row_data = self.prep_table_data_for_merge(invoice_proxy=invoice_proxy)

        document = MailMerge(self.file_path)
        document.merge(**field_data)
        document.merge_rows("date", row_data)
        document.write(output_file_path)
