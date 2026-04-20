# location_service.py
import json

def get_locations():
    with open("data/locations.json") as f:
        return json.load(f)