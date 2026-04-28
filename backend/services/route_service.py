import requests
import math
from backend.services.location_service import get_location_by_name


def _haversine_km(lat1, lng1, lat2, lng2):
    """Calculate distance in km between two coordinates."""
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def _osrm_route(lng1, lat1, lng2, lat2, alternatives=False):
    """Call OSRM API for driving route."""
    alt_param = "true" if alternatives else "false"
    url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{lng1},{lat1};{lng2},{lat2}"
        f"?overview=full&geometries=geojson&alternatives={alt_param}"
    )
    try:
        res = requests.get(url, timeout=30)
        data = res.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            return None
        return data
    except Exception as e:
        print(f"OSRM error: {e}")
        return None


def _nominatim_geocode(query):
    """Geocode address using Nominatim."""
    try:
        url = (
            f"https://nominatim.openstreetmap.org/search"
            f"?q={query.replace(' ', '+')}+Danau+Toba"
            f"&format=json&limit=1&countrycodes=id"
        )
        res = requests.get(url, headers={"User-Agent": "TobaAI/1.0"}, timeout=15)
        data = res.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lng": float(data[0]["lon"])}
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None


def _score_route(route_data, weather=None, crowd=None):
    """Score a single route with multiple factors."""
    distance = route_data.get("distance", 0)
    duration = route_data.get("duration", 0)
    
    # Get geometry for complexity analysis
    geometry = route_data.get("geometry", {})
    coordinates = geometry.get("coordinates", []) if isinstance(geometry, dict) else []
    
    # Calculate turns (simplified: count direction changes)
    turns = 0
    if len(coordinates) > 2:
        for i in range(2, len(coordinates)):
            prev = coordinates[i-1]
            curr = coordinates[i]
            if len(prev) >= 2 and len(curr) >= 2:
                # Simple direction change detection
                dlat1 = prev[1] - coordinates[i-2][1]
                dlng1 = prev[0] - coordinates[i-2][0]
                dlat2 = curr[1] - prev[1]
                dlng2 = curr[0] - prev[0]
                
                # Check if direction changed significantly
                angle1 = math.atan2(dlng1, dlat1) if (dlat1 != 0 or dlng1 != 0) else 0
                angle2 = math.atan2(dlng2, dlat2) if (dlat2 != 0 or dlng2 != 0) else 0
                angle_diff = abs(angle2 - angle1)
                if angle_diff > 0.5:  # ~30 degrees
                    turns += 1
    
    # Normalize metrics (0-1, higher is better)
    max_distance = 50000  # 50km
    max_duration = 3600   # 1 hour
    max_turns = 50
    
    distance_score = max(0, 1 - (distance / max_distance))
    duration_score = max(0, 1 - (duration / max_duration))
    simplicity_score = max(0, 1 - (turns / max_turns))
    
    # Weather and crowd bonuses
    weather_score = 0.5
    if weather:
        condition = weather.get("condition", "")
        if condition in ["Sunny", "Clear"]:
            weather_score = 1.0
        elif condition == "Cloudy":
            weather_score = 0.8
        elif condition in ["Light Rain", "Foggy"]:
            weather_score = 0.5
        else:
            weather_score = 0.3
    
    crowd_score = 0.5
    if crowd:
        level = crowd.get("level", "sedang")
        if level == "sepi":
            crowd_score = 1.0
        elif level == "sedang":
            crowd_score = 0.7
        else:
            crowd_score = 0.4
    
    # Weighted composite score
    weights = {
        "duration": 0.35,
        "distance": 0.15,
        "simplicity": 0.15,
        "weather": 0.10,
        "crowd": 0.10,
        "elevation": 0.15
    }
    
    # Elevation is hard to get without extra API, use simplicity as proxy
    elevation_score = simplicity_score
    
    composite = (
        duration_score * weights["duration"] +
        distance_score * weights["distance"] +
        simplicity_score * weights["simplicity"] +
        elevation_score * weights["elevation"] +
        weather_score * weights["weather"] +
        crowd_score * weights["crowd"]
    )
    
    return {
        "score": round(composite, 3),
        "distance_km": round(distance / 1000, 1),
        "duration_min": round(duration / 60, 1),
        "turns": turns,
        "distance_score": round(distance_score, 3),
        "duration_score": round(duration_score, 3),
        "simplicity_score": round(simplicity_score, 3),
        "weather_score": round(weather_score, 3),
        "crowd_score": round(crowd_score, 3)
    }


def calculate_smart_route(lat, lng, destination_name, area=None, weather=None, crowd=None):
    """
    Calculate smart route (road).
    
    Args:
        lat: start latitude
        lng: start longitude  
        destination_name: name of destination
        area: destination area (e.g., "Samosir", "Simalungun")
        weather: optional weather data for scoring
        crowd: optional crowd data for scoring
    
    Returns:
        dict with route info, alternatives, and smart explanation
    """
    # 1. Resolve destination coordinates
    dest = get_location_by_name(destination_name)
    
    if dest:
        dest_lat = dest.get("lat")
        dest_lng = dest.get("lng")
        dest_area = area or dest.get("area")
    else:
        # Fallback: geocode via Nominatim
        geo = _nominatim_geocode(destination_name)
        if geo:
            dest_lat = geo["lat"]
            dest_lng = geo["lng"]
            dest_area = area
        else:
            return {"error": f"Destinasi '{destination_name}' tidak ditemukan"}
    
    # 2. Get OSRM route with alternatives
    osrm_data = _osrm_route(lng, lat, dest_lng, dest_lat, alternatives=True)
    
    if not osrm_data:
        return {"error": "Gagal mendapatkan rute dari OSRM"}
    
    # 3. Score each alternative
    alternatives = []
    for i, route in enumerate(osrm_data["routes"]):
        scored = _score_route(route, weather, crowd)
        scored.update({
            "index": i,
            "path": route["geometry"]["coordinates"],
            "is_best": False
        })
        alternatives.append(scored)
    
    # 4. Determine best route
    alternatives.sort(key=lambda x: x["score"], reverse=True)
    alternatives[0]["is_best"] = True
    
    # 5. Assign labels
    if len(alternatives) > 0:
        best = alternatives[0]
        labels = []
        
        # Fastest?
        if all(best["duration_min"] <= a["duration_min"] for a in alternatives):
            labels.append("tercepat")
        
        # Shortest?
        if all(best["distance_km"] <= a["distance_km"] for a in alternatives):
            labels.append("terpendek")
        
        # Simplest?
        if all(best["turns"] <= a["turns"] for a in alternatives):
            labels.append("paling nyaman")
        
        # Best overall
        labels.append("rekomendasi terbaik")
        best["labels"] = labels
    
    # 6. Build response
    return {
        "start": {"lat": lat, "lng": lng},
        "end": {"lat": dest_lat, "lng": dest_lng},
        "destination_name": destination_name,
        "route_count": len(alternatives),
        "best": alternatives[0] if alternatives else None,
        "alternatives": alternatives,
        "waypoints": osrm_data.get("waypoints", [])
    }


def calculate_route(lat, lng, destination_name):
    """Legacy wrapper - use calculate_smart_route instead."""
    result = calculate_smart_route(lat, lng, destination_name)
    
    if result.get("error"):
        return result
    
    best = result.get("best", {})
    return {
        "start": result["start"],
        "end": result["end"],
        "path": best.get("path", []),
        "distance": best.get("distance_km", 0) * 1000,
        "duration": best.get("duration_min", 0) * 60,
    }

