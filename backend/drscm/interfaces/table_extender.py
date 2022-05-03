from __future__ import annotations
from abc import ABC, abstractmethod
from docx.table import Table, _Row
from docx.text.run import Font
from docx.styles.style import _TableStyle
import drscm.proxies as proxies


class AbstractTableExtender(ABC):
    """
    An abstract class that extends a pre-existing a docx table

    Attributes
    ----------
    table_: Table
        The table that we will be extending
    """

    table_: Table
    table_style: _TableStyle
    base_font: Font
    base_font_bold: Font

    def __init__(self, table: Table):
        self.table_ = table
        self.table_style = table.style

    @abstractmethod
    def generate(self) -> Table:
        """
        The method that holds the core logic of generating the entire table
        """


class AbstractBillsTableExtender(AbstractTableExtender):
    """
    The class that extends the table containing the amounts that will be billed

    Attributes
    ----------
    invoice_proxy: InvoiceProxy
        The invoice proxy we will be using to extend the table
    """

    invoice_proxy: proxies.InvoiceProxy

    def __init__(self, invoice_proxy: proxies.InvoiceProxy, table: Table):
        self.invoice_proxy = invoice_proxy
        super(AbstractBillsTableExtender, self).__init__(table=table)

    def add_header_row(self):
        row = self.table_.add_row()
        total_hours_worked = self.invoice_proxy.get_total_work_session_hours()
        row.cells[
            0
        ].text = f"""Consultancy: {total_hours_worked} hours
        as executed at DRS premisis in
        Doetinchem, the Netherlands"""
        row.cells[
            2
        ].text = f"{total_hours_worked * self.invoice_proxy.project.hourly_rate} €"
        self.add_blank_row()

    @abstractmethod
    def add_fixed_travel_rows(self):
        """
        Adds the row containing the fixed travel values
        """

    @abstractmethod
    def add_flexible_travel_rows(self):
        """
        Adds the row containing the flexible travel values
        """

    @abstractmethod
    def add_tax_rows(self):
        """
        Adds the row containing the tax-related values
        """

    def add_footer_row(self):
        """
        Adds the footer row containing the total
        """
        footer_row: _Row = self.table_.add_row()
        footer_row_cells = footer_row.cells
        # Add bold styling here
        footer_row_cells[0].text = "Total to be paid incl. VAT"
        footer_row_cells[2].text = f"{self.invoice_proxy.total_including_vat} €"

    def add_blank_row(self):
        """
        Adds a blank row, for style purposes
        """
        self.table_.add_row()
