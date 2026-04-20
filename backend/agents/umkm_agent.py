# umkm_agent.py
def run_umkm(plan):
    return [{"location": p["name"], "impact": "supports local business"} for p in plan]