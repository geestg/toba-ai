from backend.services.weather_service import get_weather_data

def get_weather(location_name):
    return get_weather_data(location_name)