import unittest
from util import geocode


class TestGeocode(unittest.TestCase):

    def test_billings_home(self):
        self.assertEqual(
            geocode('2965 Tartan Rd, Billings, MT 59101'),
            [45.715702, -108.4932149]
        )

    def test_invalid_address(self):
        self.assertEqual(
            geocode(''),
            None
        )

if __name__ == '__main__':
    unittest.main()
