from backend.services.location_service import locations

def run_planner(intent):

    results = []

    for loc in locations:
        score = 0

        for pref in intent["preferences"]:
            if pref in loc.get("tags", []):
                score += 20

        if intent["type"] == "exploration":
            if "hidden" in loc["tags"]:
                score += 30
            if "popular" in loc["tags"]:
                score -= 10

        score += (100 - loc["crowd"]) * 0.3

        loc_copy = loc.copy()
        loc_copy["planner_score"] = score

        results.append(loc_copy)

    return sorted(results, key=lambda x: x["planner_score"], reverse=True)