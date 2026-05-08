import json
import os

from backend.services.osm_service import fetch_osm_locations, merge_with_static

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "locations.json")


def get_locations(use_osm=True):
    """
    Get all locations.

    Returns static locations from JSON file.
    If use_osm=True and OSM fetch succeeds, merges with real-time OSM POIs.
    """
    static_locations = []

    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                static_locations = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"WARNING: Failed to load locations.json: {e}")

    if not use_osm:
        return static_locations

    # Try to fetch from OSM (with persistent cache fallback)
    try:
        osm_locations = fetch_osm_locations()
        # Always merge even if osm_locations is empty so we get persistent cache data
        merged = merge_with_static(osm_locations, static_locations)
        if merged:
            return merged
    except Exception as e:
        print(f"WARNING: OSM fetch failed, using static only: {e}")

    return static_locations


def get_location_by_name(name):
    """Find a location by name (case-insensitive)."""
    locations = get_locations()
    for loc in locations:
        if loc.get("name", "").lower() == name.lower():
            return loc
    return None

