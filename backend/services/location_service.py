import json
from pathlib import Path

# =========================================
# LOAD DESTINATIONS
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DESTINATIONS_FILE = BASE_DIR / "data" / "destinations.json"

with open(DESTINATIONS_FILE, "r", encoding="utf-8") as f:
    DESTINATIONS = json.load(f)


# =========================================
# GET ALL LOCATIONS
# =========================================

def get_locations(use_osm=False):
    """
    Get all locations/destinations.
    
    Args:
        use_osm: If True, would fetch from OSM (not implemented in this version)
    
    Returns:
        List of destination objects
    """
    return DESTINATIONS


# =========================================
# GET LOCATION BY NAME
# =========================================

def get_location_by_name(name):
    """Get a specific location by name."""
    for dest in DESTINATIONS:
        if dest.get("name", "").lower() == name.lower():
            return dest
    return None
