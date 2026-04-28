from backend.services.weather_service import get_weather_data, get_weather_suitability


def get_weather(location_name, area=None):
    """
    Get weather data for a location.
    If area is provided, uses area-specific weather patterns.
    """
    return get_weather_data(location_name, area)


def score_weather_for_destination(weather, dest_type):
    """
    Score how suitable the current weather is for a destination type.

    Args:
        weather: dict with at least "condition" key
        dest_type: destination type (nature, religious, viewpoint, etc.)

    Returns:
        float between 0.0 and 1.0
    """
    condition = weather.get("condition", "Sunny")
    return get_weather_suitability(dest_type, condition)

