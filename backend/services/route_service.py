import requests

def calculate_route(lat, lng, destination_coords=(2.6, 98.8)):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lng},{lat};{destination_coords[1]},{destination_coords[0]}?overview=full&geometries=geojson"

        res = requests.get(url).json()

        # VALIDASI
        if "routes" not in res or len(res["routes"]) == 0:
            return {
                "error": "Route tidak ditemukan",
                "start": {"lat": lat, "lng": lng},
                "end": destination_coords
            }

        route = res["routes"][0]

        return {
            "start": {"lat": lat, "lng": lng},
            "end": destination_coords,
            "path": route["geometry"]["coordinates"],
            "distance": route["distance"],
            "duration": route["duration"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }