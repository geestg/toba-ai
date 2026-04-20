# booking_agent.py
def run_booking(plan):
    return [{"location": p["name"], "hotel": "Available"} for p in plan]