# StoreLocator

A command-line tool to find the nearest store to a given address or zip code from a CSV of stores.

## Getting Started

To get started clone this repo, and if you don't want to install all the dependencies globally (and you shouldn't want to), make sure you have something like Virtualenv installed on your machine.

### Prerequisites

To avoid potential conflicts, create a virtual environment and activate it before following installation instructions.

```
virtualenv env
. env/bin/activate
```

### Installing

Follow these steps to setup StoreLocator.

Install dependencies

```
pip install -r requirements.txt
```

Populate config variables in constants.py if you not planning on using the provided defaults.

```
# Config

STORES_CSV = 'store-locations.csv'
DEFAULT_OUTPUT = 'text'
DEFAULT_UNITS = 'mi'
DEFAULT_ENCODING = 'utf-8-sig'
DEFAULT_DELIMITER = ','
DISTANCE_PRECISION = 2

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
```

Once you are all set up, you can use StoreLocator to find the nearest store by address or zip code. Optionally, you can also choose the units for distance (mi or km) and the format you want your results outputted as (text or json).

```
Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>          Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address            Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
```

## Running the tests

```
nose2
```

## Authors

* Austin Brown
