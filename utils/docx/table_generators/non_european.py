from .dutch import DutchBillsTableExtender


class NonEuropeanBillsTableExtender(DutchBillsTableExtender):
    def add_tax_rows(self):
        """
        No VAT for non european clients
        """
        pass
