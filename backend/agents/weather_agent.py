import json
from pathlib import Path

# =========================================
# LOAD WEATHER DATA
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
WEATHER_FILE = BASE_DIR / "data" / "weather.json"

with open(WEATHER_FILE, "r", encoding="utf-8") as f:
    WEATHER_DATA = json.load(f)


# =========================================
# GET WEATHER
# =========================================

def get_weather(destination_name):
    """Get weather data for a destination."""
    return WEATHER_DATA.get(destination_name, {
        "condition": "Unknown",
        "temperature": 0
    })


# =========================================
# SCORE WEATHER FOR DESTINATION
# =========================================

def score_weather_for_destination(destination, weather):
    """
    Score weather suitability (0-1).
    Clear/sunny = good, light rain/cloudy = okay, heavy rain/foggy = poor
    """
    condition = weather.get("condition", "Unknown").lower()
    
    if condition in ["cerah", "sunny", "clear"]:
        return 0.9
    elif condition in ["berawan", "cloudy"]:
        return 0.7
    elif condition in ["berkabut", "foggy"]:
        return 0.5
    elif condition in ["hujan ringan", "light rain"]:
        return 0.4
    elif condition in ["hujan", "rain", "heavy rain"]:
        return 0.2
    else:
        return 0.5
