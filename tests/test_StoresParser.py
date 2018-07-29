from csv_parser import StoresParser
import unittest


class TestStoresParser(unittest.TestCase):
    """Test StoresParser functionality.

    """

    def setUp(self):
        """Initialize StoresParser instance with store-locations.csv.

        """

        self.sp = StoresParser('store-locations.csv')

    def test_file_path(self):
        """Test that file_path getter returns correct file_path.

        """

        self.assertEqual(self.sp.file_path, 'store-locations.csv')

    def test_encoding(self):
        """Test that encoding getter returns correct encoding.

        """

        self.assertEqual(self.sp.encoding, 'utf-8-sig')

    def test_delimiter(self):
        """Test that delimiter getter returns correct delimiter.

        """

        self.assertEqual(self.sp.delimiter, ',')

    def test_dict_initial(self):
        """Test that dict getter returns None initially before get_dict has run.

        """

        self.assertEqual(self.sp.dict, None)

    def test_get_dict(self):
        """Test that get_dict parses the csv into a list of 1791 stores.

        """

        dict = self.sp.get_dict()
        self.assertEqual(len(dict), 1791)

    def test_dict_after_get_dict(self):
        """Test that dict getter returns list of stores after get_dict has run.

        """

        dict = self.sp.get_dict()
        self.assertEqual(self.sp.dict, dict)

if __name__ == '__main__':
    unittest.main()
