import argparse
import sys
import math
import json
from csv_parser import StoresParser
from constants import STORES_CSV, DEFAULT_OUTPUT, DEFAULT_UNITS
from util import (
    format_result,
    calculate_distance,
    find_nearest_store,
    validate_args,
    geocode
)


def find_store(
        query,
        units=DEFAULT_UNITS,
        output=DEFAULT_OUTPUT,
        stores_csv=STORES_CSV):
    if units is None:
        units = DEFAULT_UNITS
    if output is None:
        output = DEFAULT_OUTPUT
    stores = StoresParser(stores_csv).get_dict()
    lat_lng = geocode(query)
    result, distance = find_nearest_store(lat_lng, stores, units)
    return format_result(result, distance, units, output)


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--address",
        help="Address used to find nearest store.",
        required=False,
    )

    parser.add_argument(
        "--zip",
        help="Zipcode used to find nearest store.",
        required=False,
    )

    parser.add_argument(
        "--units",
        help="Units used to display distance (mi|km).",
        required=False,
    )

    parser.add_argument(
        "--output",
        help="Format of outputted result (text|json).",
        required=False,
    )

    args = parser.parse_args()

    validation = validate_args(args)

    if validation['is_valid']:
        print(find_store(
            validation['query'],
            args.units,
            args.output
        ))

if __name__ == '__main__':
    main(sys.argv)
