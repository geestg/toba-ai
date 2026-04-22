def plan_trip(destinations):
    return {
        "day_1": destinations[0]["name"],
        "day_2": destinations[1]["name"] if len(destinations) > 1 else None,
        "day_3": destinations[2]["name"] if len(destinations) > 2 else None
    }