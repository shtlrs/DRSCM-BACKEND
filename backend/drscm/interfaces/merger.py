from abc import ABC, abstractmethod
from typing import List


class DocumentMerger(ABC):
    """
    An abstract word document merger
    """

    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def merge(self, output_file_path: str, *args, **kwargs):
        """
        Preps the Word document for merging and does the magic
        """
        pass

    @abstractmethod
    def prep_data_for_merge(self, *args, **kwargs) -> dict:
        """
        Preps the data necessary used to populate scattered field in the document
        """
        pass

    @abstractmethod
    def prep_table_data_for_merge(self, *args, **kwargs) -> List[dict]:
        """
        Preps the data necessary used to populate tables in the document
        """
        pass
