import os
import json

DATA_FILE = "data/locations.json"

def get_locations():
    if not os.path.exists(DATA_FILE):
        print("WARNING: locations.json not found")
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)