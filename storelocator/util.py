from storelocator.constants import (
    A,
    B,
    DEFAULT_UNITS,
    DISTANCE_PRECISION,
    DISTANCE_RADIUS,
    ESQ,
    KILOMETERS_TO_MILES,
    OUTPUT,
    STORE_FIELDS,
    UNITS
)
from decimal import (
    Decimal,
    ROUND_HALF_UP
)
import geocoder
import json
import math


def filter_stores(sp, lat_lng_ecef, initial_radius, inc_radius):
    """Queries StoresParser for stores near lat_lng_ecef within radius.

    Args:
        sp (obj): StoresParser instance.
        lat_lng_ecef (float): Converted ECEF lat/long.
        initial_radius (float): Initial search radius.
        inc_radius (float): Amount to increment search radius.
    Returns:
        List of nearby stores.

    """

    matches = []
    radius = initial_radius
    while len(matches) < 1:
        results = sp.query(lat_lng_ecef, radius)
        if results is not None:
            if len(results):
                matches.extend(results)
        radius += inc_radius
    return matches


def geodetic2ecef(lat, lon, alt=0):
    """Convert geodetic coordinates to ECEF.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        alt (float, optional): Altitude.
    Returns:
        X, Y, Z ECEF coordinates.

    """

    lat, lon = math.radians(lat), math.radians(lon)
    xi = math.sqrt(1 - ESQ * math.sin(lat))
    x = (A / xi + alt) * math.cos(lat) * math.cos(lon)
    y = (A / xi + alt) * math.cos(lat) * math.sin(lon)
    z = (A / xi * (1 - ESQ) + alt) * math.sin(lat)
    return x, y, z


def euclidean_distance(distance):
    """Return the approximate Euclidean distance
    corresponding to the given great circle distance (in km).

    Args:
        distance (float): Distance (km).
    Returns:
        Approximate Euclidean distance.

    """

    return 2 * A * math.sin(distance / (2 * B))


def geocode(query):
    """Outputs latitude and longitude for a given address or zip code.

    Args:
        query (str, int): Address or zip code.
    Returns:
        Latitude and longitude (list of floats) or None.

    """

    # TODO(Austin) Add optional parameter for provider
    g = geocoder.google(query)
    return g.latlng


def validate_args(args):
    """Validates arguments and constructs query from them.

    Args:
        args (obj): Arguments object -> address, zip, units, output.
    Returns:
        {
            is_valid: (bool),
            query: (str/int or None)
        }

    """

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
    """Formats float into rounded Decimal.

    Args:
        distance (float): Distance value to be formatted.
        precision (int, optional): Number of decimal places.
    Returns:
        Decimal representation of float rounded at given precision.

    """

    d = Decimal(distance)
    prec = '0.' + ''.join(
        ['0' if x < (precision - 1) else '1' for x in range(precision)]
    )
    return Decimal(d.quantize(Decimal(prec), rounding=ROUND_HALF_UP))


def format_result(result, distance, units, output):
    """Formats nearest store and corresponding distance into specified output.

    Args:
        result (dict or None): Result of nearest store.
        distance (float or None): Distance to nearest store.
        units (str): Distance metric (mi or km).
        output (str): Result format (text or json).
    Returns:
        Text or json representation of result and corresponding distance.

    """

    if output == 'text':
        if result is None or distance is None:
            return 'Unable to locate closest store.'
        formatted_result = (
            "Closest store is {} - {}, located in {} "
            "at {}, {}, {} {}. ({} {})"
            ).format(
            result[STORE_FIELDS['NAME']],
            result[STORE_FIELDS['LOCATION']],
            result[STORE_FIELDS['COUNTY']],
            result[STORE_FIELDS['ADDRESS']],
            result[STORE_FIELDS['CITY']],
            result[STORE_FIELDS['STATE']],
            result[STORE_FIELDS['ZIP_CODE']],
            format_distance(distance),
            units
        )
    else:
        if result is None or distance is None:
            print('Unable to locate closest store.')
            return {}
        result[STORE_FIELDS['DISTANCE']] = '{} {}'.format(
            format_distance(distance), units
        )
        formatted_result = json.dumps(result)
    return formatted_result


def calculate_distance(lat_lng_a, lat_lng_b, units=DEFAULT_UNITS):
    """Calculates distance in (mi or km) between two coords.

    Based on https://gist.github.com/rochacbruno/2883505

    Args:
        lat_lng_a (list(float)): Latitude and longitude of point A.
        lat_lng_b (list(float)): Latitude and longitude of point B.
        units (str, optional): Distance metric used for calculation (mi or km).
    Returns:
        Distance (float) in provided units (mi or km).

    """

    lat_a, lng_a = lat_lng_a
    lat_b, lng_b = lat_lng_b
    lat_diff = math.radians(lat_b - lat_a)
    lng_diff = math.radians(lng_b - lng_a)
    a = (
        math.sin(lat_diff / 2) * math.sin(lat_diff / 2) +
        math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) *
        math.sin(lng_diff / 2) * math.sin(lng_diff / 2)
        )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = DISTANCE_RADIUS * c
    if units == 'mi':
        return distance * KILOMETERS_TO_MILES
    return distance


def find_nearest_store(lat_lng, stores, units):
    """Finds store from list of stores that is closest to a given set of coords.

    Args:
        lat_lng (list(float)): Latitude and longitude being compared to.
        stores (list(dict)): List of stores to search against.
        units (str): Distance metric used for comparison.
    Returns:
        Nearest store (dict or None) and corresponding distance (float or None).

    """
    result = None
    min_distance = None
    if lat_lng is not None and stores is not None:
        for store in stores:
            store_lat_lng = [
                float(
                    store[STORE_FIELDS['LATITUDE']]
                ),
                float(store[STORE_FIELDS['LONGITUDE']])
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
