def calculate_impact(decision):
    locations = decision["full"]["plan"]
    best = decision["final_decision"]["name"]

    # Environment impact
    avg_crowd_before = sum(loc["crowd"] for loc in locations) / len(locations)
    best_loc = next(loc for loc in locations if loc["name"] == best)

    crowd_reduction = avg_crowd_before - best_loc["crowd"]

    # Economic impact (UMKM)
    umkm_boost = len(locations) * 5  # dummy boost metric

    return {
        "environment": {
            "avg_crowd": avg_crowd_before,
            "selected_location_crowd": best_loc["crowd"],
            "crowd_reduction": crowd_reduction
        },
        "economic": {
            "umkm_boost_score": umkm_boost
        }
    }