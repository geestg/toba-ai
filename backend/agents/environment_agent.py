def run_environment(plan):
    for loc in plan:
        loc["sustainability_score"] = 100 - loc["crowd"]
    return sorted(plan, key=lambda x: x["sustainability_score"], reverse=True)