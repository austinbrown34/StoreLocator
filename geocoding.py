import geocoder


def geocode(address):
    # TODO(Austin) Add optional parameter for provider
    g = geocoder.google(address)
    return g.latlng
