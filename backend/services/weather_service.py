import os
import hashlib
from datetime import datetime

import requests
from dotenv import load_dotenv

from backend.services.location_service import get_locations

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("680bcb2c1eb32b2536522fc2b24a5332")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cache untuk weather (TTL 15 menit)
_weather_cache = {}
_CACHE_TTL_MINUTES = 15

# Weather patterns per area (realistic for Danau Toba region)
AREA_WEATHER_PATTERNS = {
    "Humbang Hasundutan": {
        "base_temp": 24,
        "temp_variation": 4,
        "conditions": ["Sunny", "Cloudy", "Light Rain", "Foggy"],
        "weights": [0.45, 0.30, 0.15, 0.10]
    },
    "Samosir": {
        "base_temp": 26,
        "temp_variation": 3,
        "conditions": ["Sunny", "Cloudy", "Light Rain", "Clear"],
        "weights": [0.50, 0.25, 0.15, 0.10]
    },
    "Toba Samosir": {
        "base_temp": 25,
        "temp_variation": 3,
        "conditions": ["Sunny", "Cloudy", "Light Rain", "Clear"],
        "weights": [0.45, 0.30, 0.15, 0.10]
    },
    "Karo": {
        "base_temp": 22,
        "temp_variation": 5,
        "conditions": ["Sunny", "Cloudy", "Foggy", "Light Rain"],
        "weights": [0.35, 0.30, 0.20, 0.15]
    },
    "Simalungun": {
        "base_temp": 25,
        "temp_variation": 4,
        "conditions": ["Sunny", "Cloudy", "Light Rain", "Clear"],
        "weights": [0.45, 0.30, 0.15, 0.10]
    }
}

# Time-of-day modifiers
TIME_MODIFIERS = {
    "morning": {"temp_offset": -2, "condition_bias": "Foggy"},
    "afternoon": {"temp_offset": 3, "condition_bias": "Sunny"},
    "evening": {"temp_offset": 0, "condition_bias": "Clear"},
    "night": {"temp_offset": -3, "condition_bias": "Clear"}
}


def _get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 16:
        return "afternoon"
    elif 16 <= hour < 19:
        return "evening"
    else:
        return "night"


def _seeded_random(seed_str):
    """Generate deterministic pseudo-random value 0.0-1.0 from a seed string."""
    h = hashlib.md5(seed_str.encode()).hexdigest()
    val = int(h[:8], 16) / (2 ** 32)
    return val


def _find_location(location_name, area=None):
    locations = get_locations()
    for location in locations:
        if location_name and location.get("name", "").lower() == location_name.lower():
            return location
    return None


def _map_openweather_condition(main_condition, description=None):
    main_condition = (main_condition or "").lower()
    description = (description or "").lower()

    if main_condition == "clear":
        return "Sunny"
    if main_condition == "clouds":
        return "Cloudy"
    if main_condition in {"rain", "drizzle"}:
        return "Light Rain"
    if main_condition == "thunderstorm":
        return "Heavy Rain"
    if main_condition in {"mist", "fog", "haze", "smoke", "dust", "sand", "ash"}:
        return "Foggy"

    if "hujan" in description or "rain" in description:
        return "Light Rain"
    if "berawan" in description or "cloud" in description:
        return "Cloudy"
    if "cerah" in description or "clear" in description:
        return "Sunny"
    if "kabut" in description or "fog" in description:
        return "Foggy"

    return "Cloudy"


def _fallback_weather(location_name, area=None):
    """
    Deterministic fallback weather based on location + current hour.
    Same location at the same hour always returns the same weather.
    """
    pattern = AREA_WEATHER_PATTERNS.get(area, {
        "base_temp": 25,
        "temp_variation": 4,
        "conditions": ["Sunny", "Cloudy", "Light Rain"],
        "weights": [0.50, 0.30, 0.20]
    })

    now = datetime.now()
    time_of_day = _get_time_of_day()
    modifier = TIME_MODIFIERS.get(time_of_day, {"temp_offset": 0, "condition_bias": None})

    # Time bucket: current hour → weather stays same for entire hour
    time_bucket = now.strftime("%Y-%m-%d-%H")
    seed = f"{location_name or 'unknown'}_{area or 'unknown'}_{time_bucket}"

    # Deterministic temperature
    temp_rand = _seeded_random(seed + "_temp")
    temp_variation = (temp_rand * 2 - 1) * pattern["temp_variation"]
    temperature = round(pattern["base_temp"] + modifier["temp_offset"] + temp_variation, 1)

    # Deterministic condition
    conditions = pattern["conditions"].copy()
    weights = pattern["weights"].copy()

    if modifier["condition_bias"] and modifier["condition_bias"] in conditions:
        bias_idx = conditions.index(modifier["condition_bias"])
        weights[bias_idx] += 0.1
        total = sum(weights)
        weights = [w / total for w in weights]

    cond_rand = _seeded_random(seed + "_cond")
    cumulative = 0
    condition = conditions[0]
    for c, w in zip(conditions, weights):
        cumulative += w
        if cond_rand <= cumulative:
            condition = c
            break

    # Deterministic humidity & wind
    humidity = 65 + int(_seeded_random(seed + "_hum") * 25)
    wind_speed = 5 + int(_seeded_random(seed + "_wind") * 15)

    return {
        "location": location_name,
        "area": area,
        "temperature": temperature,
        "condition": condition,
        "time_of_day": time_of_day,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "source": "fallback"
    }


def get_weather_data(location_name, area=None, lat=None, lng=None):
    """
    Get current weather data for a location.
    Uses OpenWeather when API key is available.
    Falls back to deterministic local model.
    Cached for 15 minutes.
    """
    global _weather_cache

    cache_key = f"{location_name or ''}_{area or ''}_{lat or ''}_{lng or ''}"
    now = datetime.now()

    # Check cache
    if cache_key in _weather_cache:
        cached_data, cached_time = _weather_cache[cache_key]
        if (now - cached_time).total_seconds() < _CACHE_TTL_MINUTES * 60:
            return cached_data

    location = _find_location(location_name, area)
    if lat is None and lng is None and location:
        lat = location.get("lat")
        lng = location.get("lng")

    result = None

    if OPENWEATHER_API_KEY and lat is not None and lng is not None:
        try:
            response = requests.get(
                OPENWEATHER_URL,
                params={
                    "lat": lat,
                    "lon": lng,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric",
                    "lang": "id",
                },
                timeout=8,
            )
            response.raise_for_status()
            data = response.json()

            weather_block = (data.get("weather") or [{}])[0]
            main_condition = weather_block.get("main")
            description = weather_block.get("description")
            condition = _map_openweather_condition(main_condition, description)

            wind = data.get("wind") or {}
            main = data.get("main") or {}

            result = {
                "location": location_name,
                "area": area,
                "temperature": round(float(main.get("temp", 0.0)), 1),
                "feels_like": round(float(main.get("feels_like", main.get("temp", 0.0))), 1),
                "condition": condition,
                "description": description,
                "time_of_day": _get_time_of_day(),
                "humidity": int(main.get("humidity", 0)),
                "wind_speed": float(wind.get("speed", 0)),
                "pressure": int(main.get("pressure", 0)),
                "source": "openweather",
                "observed_at": data.get("dt"),
                "coordinates": {"lat": lat, "lng": lng},
            }
        except Exception:
            result = _fallback_weather(location_name, area)
    else:
        result = _fallback_weather(location_name, area)

    _weather_cache[cache_key] = (result, now)
    return result


def get_weather_suitability(dest_type, condition):
    """
    Score how suitable a weather condition is for a destination type.
    Returns a score between 0.0 (unsuitable) and 1.0 (perfect).
    """
    suitability_matrix = {
        "nature": {
            "Sunny": 1.0,
            "Clear": 1.0,
            "Cloudy": 0.85,
            "Light Rain": 0.5,
            "Foggy": 0.6,
            "Heavy Rain": 0.2
        },
        "religious": {
            "Sunny": 1.0,
            "Clear": 1.0,
            "Cloudy": 0.9,
            "Light Rain": 0.8,
            "Foggy": 0.7,
            "Heavy Rain": 0.5
        },
        "viewpoint": {
            "Sunny": 1.0,
            "Clear": 1.0,
            "Cloudy": 0.7,
            "Light Rain": 0.4,
            "Foggy": 0.2,
            "Heavy Rain": 0.1
        },
        "camping": {
            "Sunny": 1.0,
            "Clear": 0.95,
            "Cloudy": 0.8,
            "Light Rain": 0.5,
            "Foggy": 0.6,
            "Heavy Rain": 0.2
        },
        "beach": {
            "Sunny": 1.0,
            "Clear": 0.95,
            "Cloudy": 0.7,
            "Light Rain": 0.4,
            "Foggy": 0.3,
            "Heavy Rain": 0.1
        },
        "cultural": {
            "Sunny": 1.0,
            "Clear": 1.0,
            "Cloudy": 0.9,
            "Light Rain": 0.75,
            "Foggy": 0.7,
            "Heavy Rain": 0.5
        }
    }

    type_scores = suitability_matrix.get(dest_type, suitability_matrix["nature"])
    return type_scores.get(condition, 0.5)

