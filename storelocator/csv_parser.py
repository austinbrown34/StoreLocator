import codecs
from storelocator.constants import (
    DEFAULT_DELIMITER,
    DEFAULT_ENCODING,
    STORE_FIELDS
)
import csv
import numpy
import os
import pickle
from scipy.spatial import KDTree
from storelocator.util import (
    euclidean_distance,
    geodetic2ecef
)


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
        self.stores = None
        self.tree = None

    @staticmethod
    def get_StoresParser(stores_csv):
        if os.path.exists('{}.pkl'.format(stores_csv)):
            with open('{}.pkl'.format(stores_csv), 'rb') as input:
                sp = pickle.load(input)
        else:
            sp = StoresParser(stores_csv)
            sp.get_stores()
            sp.build_tree()
            sp.save()
        return sp

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
    def stores(self):
        """Getter for stores.

        """

        return self.__stores

    @stores.setter
    def stores(self, stores):
        """Setter for stores.

        """

        self.__stores = stores

    @property
    def tree(self):
        """Getter for tree.

        """

        return self.__tree

    @tree.setter
    def tree(self, tree):
        """Setter for tree.

        """

        self.__tree = tree

    def save(self):
        """Saves StoresParser instance to .pkl file.

        """

        with open('{}.pkl'.format(self.file_path), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def build_tree(self):
        """Creates KDTree representation of coordinate data.

        """

        if self.stores is not None:
            stores_ecef = []
            for store in self.stores:
                store_ecef = geodetic2ecef(
                    float(store[STORE_FIELDS['LATITUDE']]),
                    float(store[STORE_FIELDS['LONGITUDE']])
                )
                store['ecef'] = store_ecef
                stores_ecef.append(store_ecef)
            self.tree = KDTree(numpy.array(stores_ecef))

    def query(self, target_ecef, radius):
        """Searches for stores within a given radius of a location.

        Args:
            target_ecef (float): XYZ ECEF coords to search against.
            radius (float): Search radius.
        Returns:
            List of stores within a given radius of a location.

        """

        results = None
        if self.tree is not None:
            matches = self.tree.query_ball_point(
                [target_ecef],
                r=euclidean_distance(radius)
            )
            if len(matches):
                results = [self.stores[match] for match in matches[0]]
        return results

    def get_stores(self):
        """Parses stores data from CSV and returns a list of stores (dicts).

        The list of stores that is returned is sorted by latitude and then
        longitude.

        """

        with codecs.open(self.file_path, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            self.stores = list(reader)
        return self.stores
