from .dutch import DutchBillsTableExtender
from docx.table import _Row


class EuropeanBillsTableExtender(DutchBillsTableExtender):
    def add_tax_rows(self):
        """
        Vat is transferred if client is european
        """
        total_excl_vat_row: _Row = self.table_.add_row()
        total_excl_vat_row_cells = total_excl_vat_row.cells
        total_excl_vat_row_cells[0].text = "VAT transferred"
        self.add_blank_row()
