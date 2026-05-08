import json
from pathlib import Path


# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"


# =========================================
# LOAD JSON HELPER
# =========================================

def load_json(filename):

    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================================
# LOAD ALL DATA
# =========================================

DESTINATIONS = load_json("destinations.json")

WEATHER = load_json("weather.json")

CROWD = load_json("crowd.json")

CULINARY = load_json("culinary.json")

HOTELS = load_json("hotels.json")

ROUTES = load_json("routes.json")


# =========================================
# DESTINATION HELPERS
# =========================================

def get_all_destinations():

    return DESTINATIONS


def get_destination_by_name(text):

    text = text.lower()

    for destination in DESTINATIONS:

        if destination["name"].lower() in text:
            return destination

    return None


# =========================================
# WEATHER
# =========================================

def get_weather_by_destination(destination_name):

    return WEATHER.get(
        destination_name,
        {
            "condition": "clear",
            "temperature": 25
        }
    )


# =========================================
# CROWD
# =========================================

def get_crowd_by_destination(destination_name):

    return CROWD.get(
        destination_name,
        "medium"
    )


# =========================================
# FOOD
# =========================================

def get_food_by_destination(destination_name):

    results = []

    for item in CULINARY:

        if item["destination"].lower() == destination_name.lower():
            results.append(item)

    return results


# =========================================
# HOTELS
# =========================================

def get_hotels_by_destination(destination_name):

    results = []

    for item in HOTELS:

        if item["destination"].lower() == destination_name.lower():
            results.append(item)

    return results


# =========================================
# ROUTES
# =========================================

def get_route_data(destination_name):

    for route in ROUTES:

        if route["to"].lower() == destination_name.lower():
            return route

    return {
        "from": "Medan",
        "to": destination_name,
        "distance_km": 120,
        "duration_hours": 4,
        "traffic": "medium"
    }