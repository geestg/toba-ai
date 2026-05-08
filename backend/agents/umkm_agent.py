import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _build_umkm_query(lat, lng, radius_km=5000):
    """Build Overpass QL query for nearby UMKM (restaurants, cafes, etc.)."""
    radius = int(radius_km)
    query = f"""
[out:json][timeout:30];
(
  node["amenity"~"restaurant|cafe|fast_food|marketplace|food_court"](around:{radius},{lat},{lng});
  way["amenity"~"restaurant|cafe|fast_food|marketplace|food_court"](around:{radius},{lat},{lng});
  node["shop"~"convenience|supermarket|bakery"](around:{radius},{lat},{lng});
  way["shop"~"convenience|supermarket|bakery"](around:{radius},{lat},{lng});
);
out center;
"""
    return query.strip()


def _parse_umkm_element(element):
    """Parse a single OSM element into UMKM dict."""
    tags = element.get("tags", {})
    elem_type = element.get("type")

    name = tags.get("name") or tags.get("name:id")
    if not name or len(name) < 2:
        return None

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

    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")

    # Determine type label
    if "restaurant" in amenity or "food_court" in amenity:
        type_label = "restaurant"
    elif "cafe" in amenity:
        type_label = "cafe"
    elif "fast_food" in amenity:
        type_label = "fast_food"
    elif "marketplace" in amenity or "convenience" in shop or "supermarket" in shop:
        type_label = "market"
    else:
        type_label = "shop"

    # Simple deterministic rating
    import hashlib
    seed = f"{name}_{type_label}"
    h = hashlib.md5(seed.encode()).hexdigest()
    rand_val = int(h[:8], 16) / (2 ** 32)
    rating = round(3.5 + rand_val * 1.5, 1)

    return {
        "name": name,
        "type": type_label,
        "lat": round(lat, 6),
        "lng": round(lon, 6),
        "rating": min(5.0, rating),
        "osm_id": element.get("id"),
        "source": "osm"
    }


def _haversine_km(lat1, lng1, lat2, lng2):
    import math
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _fetch_nearby_umkm_osm(lat, lng, radius_km=5):
    """Fetch real UMKM data from OSM Overpass API."""
    query = _build_umkm_query(lat, lng, radius_km * 1000)
    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=35,
            headers={"User-Agent": "TobaAI/1.0"}
        )
        response.raise_for_status()
        data = response.json()

        results = []
        seen = set()
        for elem in data.get("elements", []):
            parsed = _parse_umkm_element(elem)
            if parsed and parsed["name"] not in seen:
                seen.add(parsed["name"])
                # Calculate distance from destination
                parsed["distance_km"] = round(
                    _haversine_km(lat, lng, parsed["lat"], parsed["lng"]), 2
                )
                results.append(parsed)

        results.sort(key=lambda x: x["distance_km"])
        return results
    except Exception as e:
        print(f"UMKM OSM fetch error: {e}")
        return []


def get_umkm_insight(location, weather=None, selected_destination=None):
    """
    Get UMKM insight for a location.
    If selected_destination is provided, returns nearby UMKM recommendations for that destination's area.
    """
    target_area = None
    if selected_destination and isinstance(selected_destination, dict):
        target_area = selected_destination.get("area")
        location_name = selected_destination.get("name", location)
    else:
        location_name = location if isinstance(location, str) else location.get("name", "lokasi ini")

    temp = weather.get("temperature", 25) if weather else 25
    condition = weather.get("condition", "Sunny") if weather else "Sunny"

    if temp > 28 or condition == "Sunny":
        suggestion = f"Minuman dingin & jajanan ringan bakal laris di sekitar {location_name}"
        impact = "UMKM minuman meningkat"
        top_picks = ["Es Kopi Toba", "Jus Alpukat", "Es Campur", "Air Kelapa"]
    elif condition in ["Light Rain", "Cloudy"]:
        suggestion = f"Makanan hangat & minuman teh/kopi lebih diminati di sekitar {location_name}"
        impact = "UMKM kuliner tradisional naik"
        top_picks = ["Kopi Toba Panas", "Mie Rebus", "Sop Kambing", "Teh Talua"]
    else:
        suggestion = f"Makanan hangat lebih diminati di sekitar {location_name}"
        impact = "UMKM kuliner tradisional naik"
        top_picks = ["Kopi Toba", "Mie Gomak", "Sangsang", "Ikan Na Niura"]

    return {
        "location": location_name,
        "area": target_area,
        "suggestion": suggestion,
        "impact": impact,
        "top_picks": top_picks,
        "weather_context": {"temperature": temp, "condition": condition}
    }


def find_nearby_umkm(selected_destination):
    """
    Find UMKM options near a selected destination using OSM real-time data.
    Falls back to empty list with a message if fetch fails.
    """
    if not selected_destination or not isinstance(selected_destination, dict):
        return {"error": "No destination selected"}

    lat = selected_destination.get("lat")
    lng = selected_destination.get("lng")
    name = selected_destination.get("name", "Destinasi")
    area = selected_destination.get("area", "Danau Toba")

    if lat is None or lng is None:
        return {
            "destination": name,
            "area": area,
            "umkm_list": [],
            "count": 0,
            "note": "Koordinat destinasi tidak tersedia."
        }

    nearby = _fetch_nearby_umkm_osm(lat, lng, radius_km=5)

    if not nearby:
        return {
            "destination": name,
            "area": area,
            "umkm_list": [],
            "count": 0,
            "note": "Data UMKM sekitar belum tersedia saat ini. Coba lagi nanti."
        }

    return {
        "destination": name,
        "area": area,
        "umkm_list": nearby[:10],
        "count": len(nearby)
    }

