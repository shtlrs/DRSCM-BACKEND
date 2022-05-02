from drscm.interfaces import AbstractBillsTableGenerator
from docx.table import Table, _Row


class DutchBillsTableGenerator(AbstractBillsTableGenerator):


    def generate(self) -> Table:
        if self.invoice_proxy.fixed_travels_proxy.exists():
            self.add_fixed_travel_rows()
            self.add_tax_rows()
            self.add_travel_costs_row()

        elif self.invoice_proxy.hourly_travels_proxy.exists():
            self.add_flexible_travel_rows()
            self.add_tax_rows()
            self.add_travel_costs_row()

        else:
            self.add_tax_rows()

        self.add_footer_row()
        return self.table_

    def add_tax_rows(self):
        total_excl_vat_row: _Row = self.table_.add_row()
        total_excl_vat_row_cells = total_excl_vat_row.cells
        total_excl_vat_row_cells[0].text = "Total excl. VAT"
        total_excl_vat_row_cells[2].text = "1.3"
        self.add_blank_row()
        vat_21_row: _Row = self.table_.add_row()
        vat_21_row_cells = vat_21_row.cells
        vat_21_row_cells[1].text = "VAT 21%"
        vat_21_row_cells[2].text = "21 amount"
        self.add_blank_row()

    def add_fixed_travel_rows(self):
        travel_fee_row: _Row = self.table_.add_row()
        travel_row_cells = travel_fee_row.cells
        travel_row_cells[0].text = "Travel fee:"
        travel_row_cells[2].text = self.invoice_proxy.get_fixed_travels_total()
        travel_row_cells[3].text = "+"
        self.add_blank_row()

    def add_travel_costs_row(self):
        travel_costs_row: _Row = self.table_.add_row()
        travel_costs_cells = travel_costs_row.cells
        travel_costs_cells[0].text = "Travel costs"
        travel_costs_cells[2].text = f"{self.invoice_proxy.get_extra_travel_costs()} €"
        travel_costs_cells[3].text = "+"
        self.add_blank_row()

    def add_flexible_travel_rows(self):
        travel_fee_row: _Row = self.table_.add_row()
        travel_row_cells = travel_fee_row.cells
        travel_row_cells[0].text = f"Travel fee: {self.invoice_proxy.get_number_of_travel_hours()} hours"
        travel_row_cells[2].text = f"{self.invoice_proxy.get_hourly_travels_total()} €"
        travel_row_cells[3].text = "+"
        self.add_blank_row()
