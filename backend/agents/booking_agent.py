import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _build_hotel_query(lat, lng, radius_km=10000):
    """Build Overpass QL query for nearby accommodation."""
    radius = int(radius_km)
    query = f"""
[out:json][timeout:30];
(
  node["tourism"~"hotel|guest_house|hostel|motel|camp_site|chalet|apartment"](around:{radius},{lat},{lng});
  way["tourism"~"hotel|guest_house|hostel|motel|camp_site|chalet|apartment"](around:{radius},{lat},{lng});
);
out center;
"""
    return query.strip()


def _parse_hotel_element(element):
    """Parse a single OSM element into hotel/accommodation dict."""
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

    tourism = tags.get("tourism", "hotel")
    stars = tags.get("stars", "")
    rooms = tags.get("rooms", "")

    # Determine type label
    type_map = {
        "hotel": "hotel",
        "guest_house": "guesthouse",
        "hostel": "hostel",
        "motel": "motel",
        "camp_site": "camping",
        "chalet": "chalet",
        "apartment": "apartment"
    }
    type_label = type_map.get(tourism, "hotel")

    # Simple deterministic rating based on stars + name
    import hashlib
    seed = f"{name}_{stars}_{rooms}"
    h = hashlib.md5(seed.encode()).hexdigest()
    rand_val = int(h[:8], 16) / (2 ** 32)
    base = 3.5
    if stars:
        try:
            base = min(5.0, 3.0 + float(stars) * 0.4)
        except ValueError:
            pass
    rating = round(base + rand_val * 0.5, 1)

    # Simple deterministic price estimate
    price_map = {
        "hotel": "Rp400.000",
        "guesthouse": "Rp250.000",
        "hostel": "Rp150.000",
        "motel": "Rp200.000",
        "camping": "Rp100.000",
        "chalet": "Rp500.000",
        "apartment": "Rp350.000"
    }
    price = price_map.get(type_label, "Rp300.000")
    if stars:
        try:
            s = int(float(stars))
            if s >= 4:
                price = "Rp600.000"
            elif s >= 3:
                price = "Rp400.000"
        except ValueError:
            pass

    return {
        "name": name,
        "type": type_label,
        "lat": round(lat, 6),
        "lng": round(lon, 6),
        "rating": min(5.0, rating),
        "price": price,
        "stars": stars,
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


def _fetch_nearby_hotels_osm(lat, lng, radius_km=10):
    """Fetch real accommodation data from OSM Overpass API."""
    query = _build_hotel_query(lat, lng, radius_km * 1000)
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
            parsed = _parse_hotel_element(elem)
            if parsed and parsed["name"] not in seen:
                seen.add(parsed["name"])
                parsed["distance_km"] = round(
                    _haversine_km(lat, lng, parsed["lat"], parsed["lng"]), 2
                )
                results.append(parsed)

        results.sort(key=lambda x: x["distance_km"])
        return results
    except Exception as e:
        print(f"Hotel OSM fetch error: {e}")
        return []


def simulate_booking(location, selected_destination=None):
    """
    Simulate booking/accommodation search.
    If selected_destination is provided, returns nearby accommodation options from OSM.
    """
    if selected_destination and isinstance(selected_destination, dict):
        target_name = selected_destination.get("name", "lokasi ini")
        target_area = selected_destination.get("area", "Danau Toba")
        lat = selected_destination.get("lat")
        lng = selected_destination.get("lng")
    else:
        target_name = location if isinstance(location, str) else location.get("name", "lokasi ini")
        target_area = "Danau Toba"
        lat = None
        lng = None

    hotels = []
    if lat is not None and lng is not None:
        hotels = _fetch_nearby_hotels_osm(lat, lng, radius_km=10)

    if not hotels:
        return {
            "destination": target_name,
            "area": target_area,
            "hotel_available": False,
            "price_estimate": "Rp350.000 / malam",
            "recommendation": target_name,
            "hotels": [],
            "count": 0,
            "note": "Data penginapan sekitar belum tersedia saat ini. Coba lagi nanti."
        }

    return {
        "destination": target_name,
        "area": target_area,
        "hotel_available": True,
        "price_estimate": hotels[0]["price"] if hotels else "Rp350.000 / malam",
        "recommendation": target_name,
        "hotels": hotels[:10],
        "count": len(hotels)
    }


def find_nearby_hotels(selected_destination):
    """
    Find accommodation options near a selected destination using OSM real-time data.
    """
    if not selected_destination or not isinstance(selected_destination, dict):
        return {"error": "No destination selected"}

    return simulate_booking(None, selected_destination)

