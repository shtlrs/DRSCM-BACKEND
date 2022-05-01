from abc import ABC, abstractmethod
from drscm.interfaces import Billable
from docx.table import Table


class AbstractTableGenerator(ABC):
    """
    An abstract class that generates a docx table

    Attributes
    ----------
    table_: Table
        The table that we will be extending
    """

    table_: Table

    def __init__(self, table: Table):
        self.table_ = table

    @abstractmethod
    def generate(self) -> Table:
        """
        The method that holds the core logic of generating the entire table
        """
        pass


class AbstractBilledAmountTableGenerator(AbstractTableGenerator):
    """
    The class that generates the table containing the amounts that will be billed

    Attributes
    ----------
    billable_: Billable
        The billable we will be using to extend the table
    """

    billable: Billable

    def __init__(self, billable: Billable, table: Table):
        self.billable_ = billable
        super(AbstractBilledAmountTableGenerator, self).__init__(table=table)

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
    def add_tax_row(self):
        """
        Adds the row containing the tax-related values
        """
        pass

    @abstractmethod
    def add_footer_row(self):
        """
        Adds the footer row containing the total
        """
        pass


    def add_blank_row(self):
        """
        Adds a blank row, for style purposes
        """
        self.table_.add_row()
