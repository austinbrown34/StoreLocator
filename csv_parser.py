import csv
import codecs
from constants import DEFAULT_ENCODING, DEFAULT_DELIMITER


class StoresParser(object):

    def __init__(
            self,
            file_path,
            encoding=DEFAULT_ENCODING,
            delimiter=DEFAULT_DELIMITER
            ):
        self.file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter
        self.dict = None

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, fp):
        self.__file_path = fp

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, enc):
        self.__encoding = enc

    @property
    def delimiter(self):
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delim):
        self.__delimiter = delim

    @property
    def dict(self):
        return self.__dict

    @dict.setter
    def dict(self, dic):
        self.__dict = dic

    def get_dict(self):
        with codecs.open(self.file_path, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            self.dict = list(reader)
        return self.dict
