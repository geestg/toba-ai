from backend.services.location_service import get_locations

def get_recommendation():
    data = get_locations()

    sorted_places = sorted(data, key=lambda x: x["rating"], reverse=True)

    return sorted_places[:3]