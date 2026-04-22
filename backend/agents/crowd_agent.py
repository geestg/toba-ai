import random
from datetime import datetime

def estimate_crowd(location_name):
    hour = datetime.now().hour

    # logika semi real-time
    if 10 <= hour <= 15:
        base = "ramai"
    elif 16 <= hour <= 18:
        base = "sedang"
    else:
        base = "sepi"

    fluctuation = random.choice(["naik", "stabil", "turun"])

    return {
        "location": location_name,
        "level": base,
        "trend": fluctuation,
        "best_time": "pagi hari" if base == "ramai" else "sekarang"
    }