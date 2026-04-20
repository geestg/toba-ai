def run_umkm(plan):
    return [{"name": l["name"], "score": 80 if l["crowd"]<50 else 60} for l in plan]