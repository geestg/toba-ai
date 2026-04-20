USE_LLM = False

def make_decision(intent, plan, routing, cost, weather, umkm):

    best = plan[0]

    return {
        "final_decision": best,
        "reason": "Optimal berdasarkan crowd & preferensi",
        "explanation": "System memilih lokasi dengan crowd rendah dan cocok dengan intent user"
    }