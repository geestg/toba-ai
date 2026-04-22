import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "locations.json")


def get_locations():
    if not os.path.exists(DATA_PATH):
        print("WARNING: locations.json not found at", DATA_PATH)
        return []

    with open(DATA_PATH, "r") as f:
        return json.load(f)