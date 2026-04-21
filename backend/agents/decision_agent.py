def decide(destinations, weather, crowd):
    best = None
    best_score = -999

    for d in destinations:
        score = d.get("score", d["rating"])

        if weather["condition"] == "Hujan":
            score -= 1

        if crowd["level"] == "ramai":
            score -= 0.5

        if score > best_score:
            best_score = score
            best = d

    return best