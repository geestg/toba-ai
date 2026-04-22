def simulate_booking(location):
    return {
        "hotel_available": True,
        "price_estimate": "Rp350.000 / malam",
        "recommendation": location.get("name")
    }