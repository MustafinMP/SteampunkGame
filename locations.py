import json

GARAGE = 'GARAGE'
GARAGE_2 = 'GARAGE_2'

data = {
    GARAGE: 'data/locations/garage.json',
    GARAGE_2: 'data/locations/garage.json'}


def get_location_data(name):
    location = data[name]
    file = open(location)
    location_data = json.load(file)
    return location_data
