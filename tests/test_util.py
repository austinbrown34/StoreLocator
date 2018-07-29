import unittest
from decimal import Decimal
from util import format_result, calculate_distance, find_nearest_store, format_distance


class TestFindNearestStore(unittest.TestCase):

    def setUp(self):
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
        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                self.stores,
                'mi'
            ),
            (self.stores[0], self.distance_mi)
        )

    def test_find_nearest_store_km_good(self):
        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                self.stores,
                'km'
            ),
            (self.stores[0], self.distance_km)
        )

    def test_find_nearest_store_lat_lng_None(self):
        self.assertEqual(
            find_nearest_store(
                None,
                self.stores,
                'mi'
            ),
            (None, None)
        )

    def test_find_nearest_store_stores_None(self):
        self.assertEqual(
            find_nearest_store(
                self.lat_lng,
                None,
                'mi'
            ),
            (None, None)
        )


class TestCalculateDistance(unittest.TestCase):

    def setUp(self):
        self.lat_lng_a = [45.7711784, -108.582727]
        self.lat_lng_b = [45.5576428, -108.3942141]
        self.lat_lng_aa = [45.7711784, -108.582727]
        self.lat_lng_bb = [45.7711784, -108.582727]
        self.distance_km = 27.89948319156871
        self.distance_mi = 17.33592977022824

    def test_calculate_distance_mi_good(self):
        self.assertEqual(
            calculate_distance(
                self.lat_lng_a,
                self.lat_lng_b,
                'mi'
            ),
            self.distance_mi
        )

    def test_calculate_distance_km_good(self):
        self.assertEqual(
            calculate_distance(
                self.lat_lng_a,
                self.lat_lng_b,
                'km'
            ),
            self.distance_km
        )

    def test_calculate_distance_mi_zero(self):
        self.assertEqual(
            calculate_distance(
                self.lat_lng_aa,
                self.lat_lng_bb,
                'mi'
            ),
            0
        )

    def test_calculate_distance_km_zero(self):
        self.assertEqual(
            calculate_distance(
                self.lat_lng_aa,
                self.lat_lng_bb,
                'mi'
            ),
            0
        )


class TestFormatDistance(unittest.TestCase):

    def setUp(self):
        self.distance = 2.1556

    def test_format_distance_default_prec(self):
        self.assertEqual(format_distance(self.distance), Decimal('2.16'))

    def test_format_distance_3_prec(self):
        self.assertEqual(format_distance(self.distance, 3), Decimal('2.156'))

    def test_format_distance_1_prec(self):
        self.assertEqual(format_distance(self.distance, 1), Decimal('2.2'))


class TestFormatResult(unittest.TestCase):

    def setUp(self):
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
