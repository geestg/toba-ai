def decide(scored_destinations):
    """
    Build a ranked list of destinations with scores, reasons, weather notes, and crowd notes.

    Args:
        scored_destinations: list of dicts from recommendation_agent with
                             composite_score, explanation, weather, crowd, destination

    Returns:
        list of ranked destinations with enriched metadata
    """
    if not scored_destinations:
        return []

    ranked = []
    for i, item in enumerate(scored_destinations):
        dest = item["destination"]
        weather = item["weather"]
        crowd = item["crowd"]

        # Weather note
        condition = weather.get("condition", "Unknown")
        temp = weather.get("temperature", 0)
        weather_note = f"{condition}, {temp}°C"
        if condition in ["Sunny", "Clear"]:
            weather_note += " — cuaca ideal"
        elif condition in ["Cloudy"]:
            weather_note += " — masih nyaman"
        elif condition in ["Light Rain", "Foggy"]:
            weather_note += " — bawa pelindung"
        else:
            weather_note += " — perhatikan kondisi"

        # Crowd note
        level = crowd.get("level", "unknown")
        trend = crowd.get("trend", "stabil")
        best_time = crowd.get("best_time", "sekarang")
        crowd_note = f"{level.title()} (trend: {trend}) — {best_time}"

        ranked.append({
            "rank": i + 1,
            "name": dest.get("name"),
            "type": dest.get("type"),
            "rating": dest.get("rating"),
            "lat": dest.get("lat"),
            "lng": dest.get("lng"),
            "score": item.get("composite_score", 0),
            "reason": item.get("explanation", ""),
            "weather_note": weather_note,
            "crowd_note": crowd_note,
            "weather": weather,
            "crowd": crowd,
            "area": dest.get("area"),
            "accessibility": dest.get("accessibility"),
            "tags": dest.get("category_tags", [])
        })

    return ranked

