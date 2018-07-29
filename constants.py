# Don't Change

KILOMETERS_TO_MILES = 0.621371
DISTANCE_RADIUS = 6371
UNITS = ['mi', 'km']
OUTPUT = ['text', 'json']

# Constants defined by the World Geodetic System 1984 (WGS84)
A = 6378.137
B = 6356.7523142
ESQ = 6.69437999014 * 0.001

# Config

STORES_CSV = 'store-locations.csv'
DEFAULT_OUTPUT = 'text'
DEFAULT_UNITS = 'mi'
DEFAULT_ENCODING = 'utf-8-sig'
DEFAULT_DELIMITER = ','
DISTANCE_PRECISION = 2
INITIAL_RADIUS = 100
INC_RADIUS = 100

# CSV Field Names
STORE_FIELDS = {
    'NAME': 'Store Name',
    'LOCATION': 'Store Location',
    'COUNTY': 'County',
    'ADDRESS': 'Address',
    'CITY': 'City',
    'STATE': 'State',
    'ZIP_CODE': 'Zip Code',
    'LATITUDE': 'Latitude',
    'LONGITUDE': 'Longitude',
    'DISTANCE': 'Distance'
}
