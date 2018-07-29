import codecs
from constants import (
    DEFAULT_DELIMITER,
    DEFAULT_ENCODING
)
import csv


class StoresParser(object):
    """StoresParser converts a CSV of stores data into a list of stores.

    """

    def __init__(
            self,
            file_path,
            encoding=DEFAULT_ENCODING,
            delimiter=DEFAULT_DELIMITER
            ):
        """Initialization creates a StoresParser instance to parse provided CSV.

        StoresParser is initialized with a relative file path to a CSV
        containing data about stores.  Optionally, the encoding of the CSV
        and the field delimiter may be passed to dictate how the CSV will
        be parsed.

        Args:
            file_path (str): Relative path to the CSV.
            encoding (str, optional): Encoding of the CSV.
            delimiter (str, optional): Field delimiter of the CSV.

        """
        self.file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter
        self.dict = None

    @property
    def file_path(self):
        """Getter for file_path.

        """

        return self.__file_path

    @file_path.setter
    def file_path(self, fp):
        """Setter for file_path.

        """

        self.__file_path = fp

    @property
    def encoding(self):
        """Getter for encoding.

        """

        return self.__encoding

    @encoding.setter
    def encoding(self, enc):
        """Setter for encoding.

        """

        self.__encoding = enc

    @property
    def delimiter(self):
        """Getter for delimiter.

        """

        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delim):
        """Setter for delimiter.

        """

        self.__delimiter = delim

    @property
    def dict(self):
        """Getter for dict.

        """

        return self.__dict

    @dict.setter
    def dict(self, dic):
        """Setter for dict.

        """

        self.__dict = dic

    def get_dict(self):
        """Parses stores data from CSV and returns a list of stores (dicts).

        """

        with codecs.open(self.file_path, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            self.dict = list(reader)
        return self.dict
