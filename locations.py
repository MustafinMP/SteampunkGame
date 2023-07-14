import json

GARAGE = 0
GARAGE_2 = 1

locations = {
    GARAGE: 'data/locations/garage.json',
    GARAGE_2: 'data/locations/garage.json'}

location_keys = {'GARAGE': GARAGE,
                 'GARAGE_2': GARAGE_2}


def get_key(name):
    return location_keys[name]


def get(name):
    location = locations[name]
    file = open(location)
    location_data = json.load(file)
    return location_data
