import requests
import hashlib
import os
import json
from datetime import datetime

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Cache
_osm_cache = {}
_OSM_CACHE_TTL_MINUTES = 60

# Persistent cache file
_PERSISTENT_CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_PERSISTENT_CACHE_PATH = os.path.join(_PERSISTENT_CACHE_DIR, "osm_cache.json")
_PERSISTENT_CACHE_TTL_MINUTES = 60 * 24 * 7  # 7 days

# Bounding box Danau Toba (approximate)
DANAU_TOBA_BBOX = {
    "south": 2.30,
    "west": 98.40,
    "north": 2.90,
    "east": 99.00
}

# OSM tourism tags -> our type mapping (base)
TOURISM_TYPE_MAP = {
    "attraction": "nature",
    "viewpoint": "viewpoint",
    "museum": "cultural",
    "hotel": "hotel",
    "guest_house": "hotel",
    "camp_site": "camping",
    "picnic_site": "nature",
    "artwork": "cultural",
    "information": "cultural",
    "theme_park": "nature",
    "zoo": "nature",
    "aquarium": "nature",
}

# Placeholder images per type
TYPE_PLACEHOLDER = {
    "nature": "/images/placeholder-nature.jpg",
    "viewpoint": "/images/placeholder-viewpoint.jpg",
    "cultural": "/images/placeholder-cultural.jpg",
    "religious": "/images/placeholder-religious.jpg",
    "beach": "/images/placeholder-beach.jpg",
    "camping": "/images/placeholder-camping.jpg",
    "hotel": "/images/placeholder-hotel.jpg",
}


def _load_persistent_cache():
    """Load OSM data from persistent disk cache if still fresh."""
    if not os.path.exists(_PERSISTENT_CACHE_PATH):
        return None
    try:
        with open(_PERSISTENT_CACHE_PATH, "r", encoding="utf-8") as f:
            cache_entry = json.load(f)
        cached_time = datetime.fromisoformat(cache_entry["cached_at"])
        age_minutes = (datetime.now() - cached_time).total_seconds() / 60
        if age_minutes < _PERSISTENT_CACHE_TTL_MINUTES:
            return cache_entry.get("data", [])
    except Exception as e:
        print(f"WARNING: Failed to load persistent OSM cache: {e}")
    return None


def _save_persistent_cache(data):
    """Save OSM data to persistent disk cache."""
    try:
        os.makedirs(_PERSISTENT_CACHE_DIR, exist_ok=True)
        cache_entry = {
            "cached_at": datetime.now().isoformat(),
            "data": data
        }
        with open(_PERSISTENT_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache_entry, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"WARNING: Failed to save persistent OSM cache: {e}")


def _build_overpass_query(bbox):
    """Build Overpass QL query for tourism POIs in bounding box."""
    s, w, n, e = bbox["south"], bbox["west"], bbox["north"], bbox["east"]

    query = f"""
[out:json][timeout:30];
(
  node["tourism"~"attraction|viewpoint|museum|camp_site|picnic_site|artwork|information|theme_park|zoo|aquarium"]({s},{w},{n},{e});
  way["tourism"~"attraction|viewpoint|museum|camp_site|picnic_site|artwork|information|theme_park|zoo|aquarium"]({s},{w},{n},{e});
  relation["tourism"~"attraction|viewpoint|museum|camp_site|picnic_site|artwork|information|theme_park|zoo|aquarium"]({s},{w},{n},{e});
);
out center;
"""
    return query.strip()


def _deterministic_rating(name, tags):
    """
    Generate a deterministic rating (3.5-5.0) based on OSM tag quality.
    Same name + tags always produces same rating.
    """
    # Seed from name + sorted tag keys
    tag_keys = "|".join(sorted(tags.keys()))
    seed_str = f"{name}_{tag_keys}"
    h = hashlib.md5(seed_str.encode()).hexdigest()
    rand_val = int(h[:8], 16) / (2 ** 32)  # 0.0 - 1.0

    # Base from tag quality signals
    base = 3.5
    if tags.get("wikidata") or tags.get("wikipedia"):
        base += 0.4
    if tags.get("website") or tags.get("contact:website"):
        base += 0.2
    if tags.get("fee") == "yes":
        base += 0.15
    if len(tags) > 12:
        base += 0.15
    if tags.get("image") or tags.get("wikimedia_commons"):
        base += 0.1

    # Add deterministic variation (0.0 - 0.5)
    variation = rand_val * 0.5
    score = base + variation
    return round(min(5.0, max(3.5, score)), 1)


def _determine_type(tags):
    """
    Determine destination type using supplementary OSM tags first,
    then name-based keywords, then fallback to tourism tag mapping.
    """
    name = (tags.get("name") or "").lower()

    # Supplementary tag detection (priority)
    if tags.get("religion") or tags.get("building") in ["church", "temple", "mosque"]:
        return "religious"

    if tags.get("historic"):
        return "cultural"

    if tags.get("natural") == "beach" or tags.get("beach") == "yes":
        return "beach"

    if tags.get("amenity") == "place_of_worship":
        return "religious"

    # Name-based keyword detection
    cultural_keywords = ["museum", "huta", "bolon", "batak", "grave", "tomb", "makam",
                         "batu", "stone", "chair", "sitio", "heritage", "situs"]
    religious_keywords = ["gereja", "church", "biara", "monastery", "kloster", "vihara",
                          "mosque", "masjid", "temple", "candi", " shrine", "patung yesus"]
    beach_keywords = ["pantai", "beach", "pasir"]
    camping_keywords = ["camp", "camping", "tenda"]

    if any(kw in name for kw in cultural_keywords):
        return "cultural"
    if any(kw in name for kw in religious_keywords):
        return "religious"
    if any(kw in name for kw in beach_keywords):
        return "beach"
    if any(kw in name for kw in camping_keywords):
        return "camping"

    # Fallback to tourism tag mapping
    tourism_tag = tags.get("tourism", "attraction")
    return TOURISM_TYPE_MAP.get(tourism_tag, "nature")


def _parse_osm_element(element):
    """Parse a single OSM element into our location format."""
    tags = element.get("tags", {})
    elem_type = element.get("type")

    # Skip unnamed or very incomplete entries
    name = tags.get("name") or tags.get("name:id")
    if not name or len(name) < 2:
        return None

    # Get coordinates
    if elem_type == "node":
        lat = element.get("lat")
        lon = element.get("lon")
    elif "center" in element:
        lat = element["center"].get("lat")
        lon = element["center"].get("lon")
    else:
        return None

    if lat is None or lon is None:
        return None

    # Determine type with supplementary tags
    dest_type = _determine_type(tags)

    # Determine area from coordinates
    area = _guess_area(lat, lon)

    # Build location dict matching our schema
    location = {
        "name": name,
        "rating": _deterministic_rating(name, tags),
        "lat": round(lat, 6),
        "lng": round(lon, 6),
        "type": dest_type,
        "area": area,
        "accessibility": _estimate_accessibility(tags),
        "baseline_crowd": _estimate_baseline_crowd(tags),
        "weather_prefs": _derive_weather_prefs(dest_type),
        "category_tags": _build_category_tags(tags, dest_type),
        "image": TYPE_PLACEHOLDER.get(dest_type, "/images/placeholder-nature.jpg"),
        "osm_id": element.get("id"),
        "osm_type": elem_type,
        "source": "osm"
    }

    return location


def _guess_area(lat, lng):
    """Rough area guess based on coordinates around Danau Toba."""
    if lat > 2.75:
        return "Karo"
    elif lat > 2.60 and lng < 98.75:
        return "Samosir"
    elif lat > 2.60:
        return "Simalungun"
    elif lat > 2.45:
        return "Toba Samosir"
    else:
        return "Humbang Hasundutan"


def _derive_weather_prefs(dest_type):
    """Derive preferred weather conditions from destination type."""
    prefs = {
        "nature": ["sunny", "cloudy"],
        "viewpoint": ["sunny", "cloudy", "clear"],
        "cultural": ["sunny", "cloudy", "light_rain"],
        "religious": ["sunny", "cloudy", "light_rain"],
        "beach": ["sunny", "cloudy"],
        "camping": ["sunny", "cloudy", "clear_night"],
        "hotel": ["sunny", "cloudy", "light_rain"],
    }
    return prefs.get(dest_type, ["sunny", "cloudy"])


def _estimate_accessibility(tags):
    """Estimate accessibility score from OSM tags."""
    if tags.get("wheelchair") == "yes":
        return 0.9
    if tags.get("access") == "yes":
        return 0.8
    if tags.get("highway") or tags.get("surface"):
        return 0.7
    return 0.5


def _estimate_baseline_crowd(tags):
    """Estimate baseline crowd from OSM popularity signals."""
    if tags.get("wikidata") or tags.get("wikipedia"):
        return 0.7
    if tags.get("fee") == "yes":
        return 0.6
    return 0.4


def _build_category_tags(tags, dest_type):
    """Build category tags array from OSM tags."""
    categories = [dest_type]

    if tags.get("natural") == "beach":
        categories.append("beach")
    if tags.get("historic"):
        categories.append("history")
    if tags.get("religion"):
        categories.append("religious")
    if tags.get("fee") == "yes":
        categories.append("paid")
    if tags.get("fee") == "no":
        categories.append("free")
    if tags.get("museum") == "yes":
        categories.append("museum")
    if "fall" in (tags.get("name") or "").lower() or tags.get("waterway") == "waterfall":
        categories.append("waterfall")

    return list(set(categories))


def fetch_osm_locations(bbox=None, use_cache=True):
    """
    Fetch tourism POIs from OpenStreetMap via Overpass API.
    Falls back to persistent disk cache if API is unreachable.

    Args:
        bbox: Optional custom bounding box dict {south, west, north, east}
        use_cache: Whether to use in-memory cached results

    Returns:
        list of location dicts, or empty list on total failure
    """
    global _osm_cache

    bbox = bbox or DANAU_TOBA_BBOX
    cache_key = f"osm_{bbox['south']}_{bbox['west']}_{bbox['north']}_{bbox['east']}"
    now = datetime.now()

    # Check in-memory cache
    if use_cache and cache_key in _osm_cache:
        cached_data, cached_time = _osm_cache[cache_key]
        if (now - cached_time).total_seconds() < _OSM_CACHE_TTL_MINUTES * 60:
            return cached_data

    query = _build_overpass_query(bbox)

    locations = []
    api_ok = False

    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=45,
            headers={"User-Agent": "TobaAI/1.0"}
        )
        response.raise_for_status()
        data = response.json()

        elements = data.get("elements", [])
        seen_names = set()

        for elem in elements:
            loc = _parse_osm_element(elem)
            if loc and loc["name"] not in seen_names:
                seen_names.add(loc["name"])
                locations.append(loc)

        # Sort by rating descending
        locations.sort(key=lambda x: x.get("rating", 0), reverse=True)

        api_ok = True
        print(f"OSM fetch success: {len(locations)} locations")

    except requests.exceptions.Timeout:
        print("OSM Overpass API timeout")
    except requests.exceptions.RequestException as e:
        print(f"OSM Overpass API error: {e}")
    except Exception as e:
        print(f"OSM parsing error: {e}")

    if not locations and not api_ok:
        # Try persistent disk cache
        cached = _load_persistent_cache()
        if cached is not None:
            print(f"OSM API failed — loaded {len(cached)} locations from persistent cache")
            locations = cached

    # Update caches
    if locations:
        _osm_cache[cache_key] = (locations, now)
        if api_ok:
            _save_persistent_cache(locations)

    return locations


def merge_with_static(osm_locations, static_locations):
    """
    Merge OSM locations with static locations.
    Static locations take precedence for duplicates (by name) to preserve curated data.
    """
    merged = {}

    # Add OSM first
    for loc in osm_locations:
        name = loc.get("name", "").lower().strip()
        if name:
            merged[name] = loc

    # Override with static (curated data is more trusted)
    for loc in static_locations:
        name = loc.get("name", "").lower().strip()
        if name:
            merged[name] = {**loc, "source": "static"}

    return list(merged.values())

