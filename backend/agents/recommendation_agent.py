import math
from backend.services.location_service import get_locations
from backend.agents.weather_agent import get_weather, score_weather_for_destination
from backend.agents.crowd_agent import estimate_crowd


def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance in km between two coordinates."""
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def normalize_value(value, min_val, max_val):
    """Normalize a value to 0-1 range."""
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)


def get_recommendation(user_lat=None, user_lng=None, consider_distance=False, top_n=5):
    """
    Get multi-factor scored recommendations.

    Scoring weights:
    - rating: 0.3
    - distance: 0.2 (closer is better) — ONLY if consider_distance=True
    - weather_fit: 0.2
    - crowd: 0.2 (less crowded is better, but not empty)
    - accessibility: 0.1

    Args:
        consider_distance: If True, use user_lat/lng to bias toward nearby places.
                          If False, treat all locations equally in terms of distance.
    """
    data = get_locations()

    if not data:
        return []

    # Gather weather and crowd data for all locations
    scored_destinations = []

    for dest in data:
        name = dest["name"]
        dest_type = dest.get("type", "nature")
        area = dest.get("area")
        baseline_crowd = dest.get("baseline_crowd", 0.5)
        accessibility = dest.get("accessibility", 0.5)
        rating = dest.get("rating", 0)

        # Get weather data
        weather = get_weather(name, area)
        weather_fit = score_weather_for_destination(weather, dest_type)

        # Get crowd data
        crowd = estimate_crowd(name, baseline_crowd)
        crowd_score = crowd["score"]

        # Calculate distance score ONLY if user explicitly wants nearby places
        distance_score = 0.5  # Default neutral score (no distance bias)
        if consider_distance and user_lat is not None and user_lng is not None:
            dest_lat = dest.get("lat")
            dest_lng = dest.get("lng")
            if dest_lat is not None and dest_lng is not None:
                distance_km = haversine_distance(user_lat, user_lng, dest_lat, dest_lng)
                # Convert distance to score: closer = higher score
                # Using exponential decay: score = exp(-distance/50)
                distance_score = math.exp(-distance_km / 50)

        scored_destinations.append({
            "destination": dest,
            "weather": weather,
            "crowd": crowd,
            "rating": rating,
            "weather_fit": weather_fit,
            "crowd_score": crowd_score,
            "distance_score": distance_score,
            "accessibility": accessibility
        })

    # Normalize metrics across all destinations
    ratings = [s["rating"] for s in scored_destinations]
    min_rating, max_rating = min(ratings), max(ratings)

    weather_fits = [s["weather_fit"] for s in scored_destinations]
    min_weather, max_weather = min(weather_fits), max(weather_fits)

    crowd_scores = [s["crowd_score"] for s in scored_destinations]
    min_crowd, max_crowd = min(crowd_scores), max(crowd_scores)

    accessibilities = [s["accessibility"] for s in scored_destinations]
    min_access, max_access = min(accessibilities), max(accessibilities)

    # Calculate final composite score
    WEIGHTS = {
        "rating": 0.3,
        "distance": 0.2,
        "weather_fit": 0.2,
        "crowd": 0.2,
        "accessibility": 0.1
    }

    for s in scored_destinations:
        norm_rating = normalize_value(s["rating"], min_rating, max_rating)
        norm_weather = normalize_value(s["weather_fit"], min_weather, max_weather)
        # For crowd: we want moderate crowds (not too empty, not too full)
        # Ideal crowd score is around 0.4-0.6
        crowd_val = s["crowd_score"]
        norm_crowd = 1.0 - abs(crowd_val - 0.5) * 2  # Peak at 0.5, decreases toward 0 or 1
        norm_access = normalize_value(s["accessibility"], min_access, max_access)

        composite_score = (
            norm_rating * WEIGHTS["rating"] +
            s["distance_score"] * WEIGHTS["distance"] +
            norm_weather * WEIGHTS["weather_fit"] +
            norm_crowd * WEIGHTS["crowd"] +
            norm_access * WEIGHTS["accessibility"]
        )

        s["composite_score"] = round(composite_score, 3)

        # Generate explanation
        reasons = []
        if norm_rating > 0.7:
            reasons.append(f"Rating tinggi ({s['rating']})")
        if consider_distance and s["distance_score"] > 0.7:
            reasons.append("Dekat dari lokasi Anda")
        if norm_weather > 0.7:
            reasons.append(f"Cuaca {s['weather']['condition']} cocok untuk {s['destination']['type']}")
        if 0.4 <= crowd_val <= 0.6:
            reasons.append("Tingkat keramaian nyaman")
        elif crowd_val < 0.4:
            reasons.append("Tidak terlalu ramai")
        if norm_access > 0.7:
            reasons.append("Mudah diakses")

        s["explanation"] = "; ".join(reasons) if reasons else "Destinasi menarik dengan kondisi saat ini"

    # Sort by composite score descending
    scored_destinations.sort(key=lambda x: x["composite_score"], reverse=True)

    # Return top N
    return scored_destinations[:top_n]

