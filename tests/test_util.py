from decimal import Decimal
import unittest
from storelocator.util import (
    calculate_distance,
    find_nearest_store,
    format_distance,
    format_result
)


class TestFindNearestStore(unittest.TestCase):
    """Test find_nearest_store function.

    """

    def setUp(self):
        """Setup TestFindNearestStore with default values.

        """

        self.lat_lng = [45.5576428, -108.3942141]
        self.distance_km = 27.89948319156871
        self.distance_mi = 17.33592977022824
        self.stores = [
            {
                "Store Name": "Test Store Name A",
                "Store Location": "Test Store Location",
                "Address": "Test Address",
                "City": "Test City",
                "State": "Test State",
                "Zip Code": "Test Zip Code",
                "Latitude": "45.7711784",
                "Longitude": "-108.582727",
                "County": "Test County"
            },
            {
                "Store Name": "Test Store Name B",
                "Store Location": "Test Store Location",
                "Address": "Test Address",
                "City": "Test City",
                "State": "Test State",
                "Zip Code": "Test Zip Code",
                "Latitude": "45.7711784",
                "Longitude": "-102.3942141",
                "County": "Test County"
            }
        ]

    def test_find_nearest_store_mi_good(self):
        """Test that find_nearest_store returns the right store & distance (mi).

        """

        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                self.stores,
                'mi'
            ),
            (self.stores[0], self.distance_mi)
        )

    def test_find_nearest_store_km_good(self):
        """Test that find_nearest_store returns the right store & distance (km).

        """

        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                self.stores,
                'km'
            ),
            (self.stores[0], self.distance_km)
        )

    def test_find_nearest_store_lat_lng_None(self):
        """Test that find_nearest_store returns (None, None) if lat_lng is None.

        """

        self.assertEqual(
            find_nearest_store(
                None,
                self.stores,
                'mi'
            ),
            (None, None)
        )

    def test_find_nearest_store_stores_None(self):
        """Test that find_nearest_store returns (None, None) if stores is None.

        """

        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                None,
                'mi'
            ),
            (None, None)
        )


class TestCalculateDistance(unittest.TestCase):
    """Test calculate_distance function.

    """

    def setUp(self):
        """Setup TestCalculateDistance with default values.

        """

        self.lat_lng_a = [45.7711784, -108.582727]
        self.lat_lng_b = [45.5576428, -108.3942141]
        self.lat_lng_aa = [45.7711784, -108.582727]
        self.lat_lng_bb = [45.7711784, -108.582727]
        self.distance_km = 27.89948319156871
        self.distance_mi = 17.33592977022824

    def test_calculate_distance_mi_good(self):
        """Test that calculate_distance returns correct distance (mi).

        """

        self.assertEqual(
            calculate_distance(
                self.lat_lng_a,
                self.lat_lng_b,
                'mi'
            ),
            self.distance_mi
        )

    def test_calculate_distance_km_good(self):
        """Test that calculate_distance returns correct distance (km).

        """

        self.assertEqual(
            calculate_distance(
                self.lat_lng_a,
                self.lat_lng_b,
                'km'
            ),
            self.distance_km
        )

    def test_calculate_distance_mi_zero(self):
        """Test that calculate_distance returns zero (mi) when coords are equal.

        """

        self.assertEqual(
            calculate_distance(
                self.lat_lng_aa,
                self.lat_lng_bb,
                'mi'
            ),
            0
        )

    def test_calculate_distance_km_zero(self):
        """Test that calculate_distance returns zero (km) when coords are equal.

        """

        self.assertEqual(
            calculate_distance(
                self.lat_lng_aa,
                self.lat_lng_bb,
                'mi'
            ),
            0
        )


class TestFormatDistance(unittest.TestCase):
    """Test format_distance function.

    """

    def setUp(self):
        """Setup TestFormatDistance with default values.

        """

        self.distance = 2.1556

    def test_format_distance_default_prec(self):
        """Test that format_distance returns correct Decimal with default prec.

        """

        self.assertEqual(format_distance(self.distance), Decimal('2.16'))

    def test_format_distance_3_prec(self):
        """Test that format_distance returns correct Decimal with prec 3.

        """

        self.assertEqual(format_distance(self.distance, 3), Decimal('2.156'))

    def test_format_distance_1_prec(self):
        """Test that format_distance returns correct Decimal with prec 1.

        """

        self.assertEqual(format_distance(self.distance, 1), Decimal('2.2'))


class TestFormatResult(unittest.TestCase):
    """Test format_result function.

    """

    def setUp(self):
        """Setup TestFormatResult with default values.

        """

        self.result = {
            "Store Name": "Test Store Name",
            "Store Location": "Test Store Location",
            "Address": "Test Address",
            "City": "Test City",
            "State": "Test State",
            "Zip Code": "Test Zip Code",
            "Latitude": "Test Latitude",
            "Longitude": "Test Longitude",
            "County": "Test County"
        }
        self.formatted_result_text_good = {
            'result': self.result,
            'distance': 1.1111,
            'units': 'mi',
            'output': 'text'
        }
        self.formatted_result_json_good = {
            'result': self.result,
            'distance': 2.1111,
            'units': 'km',
            'output': 'json'
        }
        self.formatted_result_result_None_text = {
            'result': None,
            'distance': 1.1111,
            'units': 'mi',
            'output': 'text'
        }
        self.formatted_result_distance_None_text = {
            'result': self.result,
            'distance': None,
            'units': 'mi',
            'output': 'text'
        }
        self.formatted_result_result_None_json = {
            'result': None,
            'distance': 1.1111,
            'units': 'mi',
            'output': 'json'
        }
        self.formatted_result_distance_None_json = {
            'result': self.result,
            'distance': None,
            'units': 'mi',
            'output': 'json'
        }

    def test_format_result_text_good(self):
        """Test that format_result returns correct text output.

        """

        args = self.formatted_result_text_good
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            'Closest store is Test Store Name - Test Store Location, located in Test County at Test Address, Test City, Test State Test Zip Code. (1.11 mi)'
        )

    def test_format_result_json_good(self):
        """Test that format_result returns correct json output.

        """

        args = self.formatted_result_json_good
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            '{"Store Name": "Test Store Name", "Store Location": "Test Store Location", "Address": "Test Address", "City": "Test City", "State": "Test State", "Zip Code": "Test Zip Code", "Latitude": "Test Latitude", "Longitude": "Test Longitude", "County": "Test County", "Distance": "2.11 km"}'
        )

    def test_format_result_result_None_text(self):
        """Test that format_result returns correct text output for None result.

        """

        args = self.formatted_result_result_None_text
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            "Unable to locate closest store."
        )

    def test_format_result_distance_None_text(self):
        """Test that format_result returns correct text output for None distance.

        """

        args = self.formatted_result_distance_None_text
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            "Unable to locate closest store."
        )

    def test_format_result_result_None_json(self):
        """Test that format_result returns correct json output for None result.

        """

        args = self.formatted_result_result_None_json
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            {}
        )

    def test_format_result_distance_None_json(self):
        """Test that format_result returns correct json output for None distance.

        """

        args = self.formatted_result_distance_None_json
        self.assertEqual(
            format_result(
                args['result'],
                args['distance'],
                args['units'],
                args['output']
            ),
            {}
        )

if __name__ == '__main__':
    unittest.main()
