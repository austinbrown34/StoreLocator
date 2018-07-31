import unittest
from storelocator.util import geocode


class TestGeocode(unittest.TestCase):
    """Test geocoding function.

    """

    def test_billings_home(self):
        """Test that address geocodes to correct coordinates.

        """

        self.assertEqual(
            geocode('2965 Tartan Rd, Billings, MT 59101'),
            [45.715702, -108.4932149]
        )

    def test_invalid_address(self):
        """Test that invalid attempt to geocode returns None.

        """

        self.assertEqual(
            geocode(''),
            None
        )

if __name__ == '__main__':
    unittest.main()
