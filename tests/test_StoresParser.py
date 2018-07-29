import unittest
from csv_parser import StoresParser


class TestStoresParser(unittest.TestCase):
    def setUp(self):
        self.sp = StoresParser('store-locations.csv')

    def test_file_path(self):
        self.assertEqual(self.sp.file_path, 'store-locations.csv')

    def test_encoding(self):
        self.assertEqual(self.sp.encoding, 'utf-8-sig')

    def test_delimiter(self):
        self.assertEqual(self.sp.delimiter, ',')

    def test_dict_initial(self):
        self.assertEqual(self.sp.dict, None)

    def test_get_dict(self):
        dict = self.sp.get_dict()
        self.assertEqual(len(dict), 1791)

    def test_dict_after_get_dict(self):
        dict = self.sp.get_dict()
        self.assertEqual(self.sp.dict, dict)

if __name__ == '__main__':
    unittest.main()
