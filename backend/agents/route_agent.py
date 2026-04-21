from backend.services.route_service import calculate_route

def get_route(lat, lng, destination_name):
    return calculate_route(lat, lng, destination_name)