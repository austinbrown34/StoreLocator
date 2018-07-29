import math
import json
from decimal import Decimal, ROUND_HALF_UP
from constants import (
    DEFAULT_UNITS,
    DISTANCE_PRECISION,
    UNITS,
    OUTPUT,
    KILOMETERS_TO_MILES,
    DISTANCE_RADIUS,
    STORE_FIELDS
)


def validate_args(args):
    is_valid = True
    query = None
    if args.address is not None:
        if not isinstance(args.address, str):
            print('--address must be a string.')
            is_valid = False
        query = args.address
    elif args.zip is not None:
        if not (isinstance(args.zip, str) or isinstance(args.zip, int)):
            print('--zip must be a string or an integer.')
            is_valid = False
        query = args.zip
    else:
        print('--address or --zip must be specified.')
        is_valid = False
    if args.units is not None:
        if args.units not in UNITS:
            print('--units must be one of the following: {}'.format(UNITS))
            is_valid = False
    if args.output is not None:
        if args.output not in OUTPUT:
            print ('--output must be one of the following: {}'.format(OUTPUT))
            is_valid = False
    return {'is_valid': is_valid, 'query': query}


def format_distance(distance, precision=DISTANCE_PRECISION):
    d = Decimal(distance)
    prec = '0.' + ''.join(
        ['0' if x < (precision - 1) else '1' for x in range(precision)]
    )
    return Decimal(d.quantize(Decimal(prec), rounding=ROUND_HALF_UP))


def format_result(result, distance, units, output):
    if output == 'text':
        if result is None or distance is None:
            return 'Unable to locate closest store.'
        formatted_result = (
            "Closest store is {} - {}, located in {} "
            "at {}, {}, {} {}. ({} {})"
            ).format(
            result['Store Name'],
            result['Store Location'],
            result['County'],
            result['Address'],
            result['City'],
            result['State'],
            result['Zip Code'],
            format_distance(distance),
            units
        )
    else:
        if result is None or distance is None:
            print('Unable to locate closest store.')
            return {}
        result['Distance'] = '{} {}'.format(format_distance(distance), units)
        formatted_result = json.dumps(result)
    return formatted_result


def calculate_distance(lat_lng_a, lat_lng_b, units=DEFAULT_UNITS):
    lat_a, lng_a = lat_lng_a
    lat_b, lng_b = lat_lng_b
    radius = 6371
    lat_diff = math.radians(lat_b - lat_a)
    lng_diff = math.radians(lng_b - lng_a)
    a = (
        math.sin(lat_diff / 2) * math.sin(lat_diff / 2) +
        math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) *
        math.sin(lng_diff / 2) * math.sin(lng_diff / 2)
        )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    if units == 'mi':
        KILOMETERS_TO_MILES = 0.621371
        return distance * KILOMETERS_TO_MILES
    return distance


def find_nearest_store(lat_lng, stores, units):
    result = None
    min_distance = None
    if lat_lng is not None and stores is not None:
        for store in stores:
            store_lat_lng = [
                float(store['Latitude']), float(store['Longitude'])
            ]
            store_distance = calculate_distance(lat_lng, store_lat_lng, units)
            if min_distance is None:
                min_distance = store_distance
                result = store
            else:
                if store_distance < min_distance:
                    min_distance = store_distance
                    result = store
    return result, min_distance
