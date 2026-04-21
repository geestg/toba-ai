import random

def estimate_crowd(location_name):
    return {
        "location": location_name,
        "level": random.choice(["sepi", "sedang", "ramai"]),
        "best_time": "pagi hari"
    }