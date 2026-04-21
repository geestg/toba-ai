import json

def get_locations():
    with open("data/locations.json", "r") as f:
        return json.load(f)