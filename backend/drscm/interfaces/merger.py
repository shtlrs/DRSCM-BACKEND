from abc import ABC, abstractmethod
from mailmerge import MailMerge


class DocumentMerger(ABC):
    """
    An abstract word document merger
    """

    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def merge(self, fields_to_merge: dict):
        """
        Merges the data provided in the word file
        """
        pass

    @abstractmethod
    def prep_data_for_merge(self, *args, **kwargs) -> dict:
        """
        Preps the data necessary for merging the word document
        """
        pass
