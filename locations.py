import json

GARAGE = 'GARAGE'
GARAGE_2 = 'GARAGE_2'
WAREHOUSE = 'WAREHOUSE'

data = {
    GARAGE: 'data/locations/garage.json',
    GARAGE_2: 'data/locations/garage.json',
    WAREHOUSE: 'data/locations/warehouse.json'}


def get_location_data(name: str) -> dict:
    location = data[name]
    file = open(location)
    location_data = json.load(file)
    return location_data
