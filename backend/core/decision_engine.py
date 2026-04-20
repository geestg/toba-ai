def get_weights(intent):
    prefs = intent.get("preferences", {})

    weights = {
        "sustainability": 0.4,
        "weather": 0.2,
        "cost": 0.2
    }

    if prefs.get("quiet"):
        weights["sustainability"] += 0.3

    if prefs.get("cheap"):
        weights["cost"] += 0.3

    if prefs.get("good_weather"):
        weights["weather"] += 0.3

    return weights


def score_location(loc, weather_data, cost_data, weights):
    score = 0

    # Sustainability
    score += loc["sustainability_score"] * weights["sustainability"]

    # Weather
    weather = next((w for w in weather_data if w["location"] == loc["name"]), {})
    if weather.get("weather") == "sunny":
        score += 100 * weights["weather"]
    else:
        score += 30 * weights["weather"]

    # Cost
    cost = next((c for c in cost_data if c["location"] == loc["name"]), {})
    if cost:
        score += (100000 - cost["cost"]) / 1000 * weights["cost"]

    return score


def make_decision(agent_outputs):
    intent = agent_outputs["intent"]
    plan = agent_outputs["plan"]
    weather = agent_outputs["weather"]
    cost = agent_outputs["cost"]

    weights = get_weights(intent)

    scored = []

    for loc in plan:
        s = score_location(loc, weather, cost, weights)
        scored.append({
            "name": loc["name"],
            "score": round(s, 2),
            "data": loc
        })

    best = max(scored, key=lambda x: x["score"])

    return {
        "final_decision": best["data"],
        "score": best["score"],
        "weights_used": weights,
        "ranking": scored,
        "reason": "Dynamic decision based on user preferences and sustainability",
        "full": agent_outputs
    }