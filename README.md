# StoreLocator

A command-line tool to find the nearest store to a given address or zip code from a CSV of stores.

## Getting Started

To get started clone this repo, and if you don't want to install all the dependencies globally (and you shouldn't want to), make sure you have something like Virtualenv installed on your machine.

### Prerequisites

To avoid potential conflicts, create a virtual environment and activate it before following installation instructions.

```
virtualenv -p python3 env
. env/bin/activate
```

### Installing

Follow these steps to setup StoreLocator.

```
pip install storelocator
```

### Optional Setup

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

If you have cloned this repo and installed dependencies from requirements.txt you can run tests like so:

```
nose2
```

## About StoreLocator

StoreFinder was built to be flexible and scalable enough to allow for the cli functionality to be easily extended, to work with larger datasets than the one provided, and to be included modularly for use outside of the command prompt.

There are many different approaches one can take to find the nearest point in a dataset, and certainly there are improvements that can be made to this approach.

StoreFinder handles addresses and zip codes in very much the same way. Both pass through a geocoding service (default is google but other providers can easily be used) and are converted, if possible, to a latitudinal and longitudinal coordinate.

The parsing of the csv containing store location data is handled via the StoresParser object. The StoresParser reads in the csv and creates a list of stores (dicts). At the same time, the latitudinal and longitudinal coordinates for all of the stores are spatially indexed via a KDTree implementation on the StoresParser object.

By utilizing a KDTree data structure, querying for the nearest store is optimized to an Nlog(n) time complexity, reducing the number of distance calculations needed to calculated to find the nearest store. Building this tree does come with the added cost of space for storing the tree and the time required initially to populate the tree.

To benefit from this approach it was important to make sure that the KDTree did not have to repopulate every time a new search was conducted. To achieve this, the StoresParser has a save method that saves the current instance to a .pkl file once the KDTree is populated. Then, StoresParser has a static method called get_StoresParser that returns either a saved instance of StoresParser, or if no .pkl file exists, returns a new instance after it populates its KDTree.

In order for lat/lon coordinates to be stored in a KDTree and spatially represented accurately, they have to be converted to a new type of coordinates (ECEF X, Y, Z) that can be used to calculate euclidean distances.

Finding the nearest store first queries the tree to receive the closest possible results, then from that list of results, a traditional brute-force and iterative comparison is conducted to find the closest.

Distance calculations are based of the Haversine formula.

https://en.wikipedia.org/wiki/Haversine_formula

## Authors

* Austin Brown
