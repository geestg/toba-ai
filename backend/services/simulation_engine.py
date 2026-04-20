def simulate(decision):
    locations = decision["full"]["plan"]

    before = {}
    after = {}

    total_visitors = 100  # asumsi total wisatawan

    # BEFORE (distribusi asli berdasarkan crowd)
    total_crowd = sum(loc["crowd"] for loc in locations)

    for loc in locations:
        before[loc["name"]] = round((loc["crowd"] / total_crowd) * total_visitors)

    # AFTER (redistribusi ke tempat terbaik)
    best = decision["final_decision"]["name"]

    for loc in locations:
        if loc["name"] == best:
            after[loc["name"]] = before[loc["name"]] + 20
        else:
            after[loc["name"]] = max(0, before[loc["name"]] - 10)

    return {
        "before": before,
        "after": after,
        "best_location": best
    }