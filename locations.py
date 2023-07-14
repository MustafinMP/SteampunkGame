import json

GARAGE = 0

locations = {
    GARAGE: 'data/locations/garage.json'}


def get(name):
    location = locations[name]
    file = open(location)
    location_data = json.load(file)
    return location_data