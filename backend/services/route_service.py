import requests

def calculate_route(lat, lng, destination_coords=(2.6, 98.8)):
    url = f"http://router.project-osrm.org/route/v1/driving/{lng},{lat};{destination_coords[1]},{destination_coords[0]}?overview=full&geometries=geojson"

    res = requests.get(url).json()

    coords = res["routes"][0]["geometry"]["coordinates"]

    return {
        "start": {"lat": lat, "lng": lng},
        "end": destination_coords,
        "path": coords,
        "distance": res["routes"][0]["distance"],
        "duration": res["routes"][0]["duration"]
    }