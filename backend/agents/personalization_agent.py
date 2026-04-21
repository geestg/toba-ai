def personalize(destinations, user_memory):
    prefs = user_memory.get("preferences", {})

    for d in destinations:
        score = d["rating"]

        if prefs.get("prefer_cool") and d["temperature"] < 26:
            score += 0.5

        if prefs.get("avoid_hot") and d["temperature"] > 28:
            score -= 0.5

        d["score"] = score

    return sorted(destinations, key=lambda x: x["score"], reverse=True)