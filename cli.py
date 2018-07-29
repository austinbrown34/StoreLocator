import argparse
from constants import (
    DEFAULT_OUTPUT,
    DEFAULT_UNITS,
    STORES_CSV
)
from csv_parser import StoresParser
import sys
from util import (
    find_nearest_store,
    format_result,
    geocode,
    validate_args
)


def find_store(
        query,
        units=DEFAULT_UNITS,
        output=DEFAULT_OUTPUT,
        stores_csv=STORES_CSV):
    """Outputs nearest store to address or zip code from CSV of stores.

    Args:
        query (str, int): Address or zip code.
        units (str, optional): Distance measurement (mi or km).
        output (str, optional): Result format (text or json).
        stores_csv (str): Relative path to csv containing stores data.
    Returns:
        Text or json representation of nearest store and distance.

    """

    if units is None:
        units = DEFAULT_UNITS
    if output is None:
        output = DEFAULT_OUTPUT
    stores = StoresParser(stores_csv).get_dict()
    lat_lng = geocode(query)
    result, distance = find_nearest_store(lat_lng, stores, units)
    return format_result(result, distance, units, output)


def main(argv):
    """Command-line interface to find nearest store from address or zip code.

    Args:
        --address (str, optional): Address used to find nearest store.
        --zip (str or int, optional): Zip code used to find nearest store.
        --units (str, optional): Distance metric (mi or km).
        --output (str, optional): Result format (text json).
    Returns:
        Output from find_store given user input arguments.

    """
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
