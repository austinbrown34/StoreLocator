from storelocator.csv_parser import StoresParser
from storelocator.constants  import STORES_CSV
import unittest


class TestStoresParser(unittest.TestCase):
    """Test StoresParser functionality.

    """

    def setUp(self):
        """Initialize StoresParser instance with store-locations.csv.

        """

        self.sp = StoresParser(STORES_CSV)

    def test_file_path(self):
        """Test that file_path getter returns correct file_path.

        """

        self.assertEqual(self.sp.file_path, STORES_CSV)

    def test_encoding(self):
        """Test that encoding getter returns correct encoding.

        """

        self.assertEqual(self.sp.encoding, 'utf-8-sig')

    def test_delimiter(self):
        """Test that delimiter getter returns correct delimiter.

        """

        self.assertEqual(self.sp.delimiter, ',')

    def test_stores_initial(self):
        """Test that stores getter returns None initially before get_stores has run.

        """

        self.assertEqual(self.sp.stores, None)

    def test_get_stores(self):
        """Test that get_stores parses the csv into a list of 1791 stores.

        """

        stores = self.sp.get_stores()
        self.assertEqual(len(stores), 1791)

    def test_stores_after_get_stores(self):
        """Test that stores getter returns list of stores after get_stores has run.

        """

        stores = self.sp.get_stores()
        self.assertEqual(self.sp.stores, stores)

if __name__ == '__main__':
    unittest.main()
