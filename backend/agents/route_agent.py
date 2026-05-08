from backend.services.route_service import calculate_smart_route


def get_route(lat, lng, destination_name, area=None, weather=None, crowd=None):
    """
    Get smart route with multi-modal support and natural language explanation.
    
    Args:
        lat: start latitude
        lng: start longitude
        destination_name: name of destination
        area: destination area
        weather: optional weather data
        crowd: optional crowd data
    
    Returns:
        dict with route data and natural language explanation
    """
    result = calculate_smart_route(lat, lng, destination_name, area, weather, crowd)
    
    if result.get("error"):
        return {
            "error": result["error"],
            "explanation": f"❌ {result['error']}"
        }
    
    # Build natural language explanation
    explanation = _build_explanation(result, destination_name)
    
    return {
        **result,
        "explanation": explanation
    }


def _build_explanation(result, destination_name):
    """Build natural language explanation for the route."""
    return _build_road_explanation(result, destination_name)


def _build_road_explanation(result, destination_name):
    """Build explanation for pure road route."""
    best = result.get("best", {})
    
    if not best:
        return f"Rute ke {destination_name} tidak dapat dihitung."
    
    lines = [
        f"🛣️ **Rute ke {destination_name}**",
        "",
        f"📍 Jarak: {best.get('distance_km', 0)} km",
        f"⏱️ Estimasi waktu: {best.get('duration_min', 0)} menit",
    ]
    
    labels = best.get("labels", [])
    if labels:
        lines.append(f"🏷️ Label: {', '.join(labels)}")
    
    # Add alternatives info
    alternatives = result.get("alternatives", [])
    if len(alternatives) > 1:
        lines.append("")
        lines.append("📋 **Alternatif rute:**")
        for i, alt in enumerate(alternatives[1:3], 2):
            lines.append(
                f"   {i}. {alt.get('distance_km', 0)} km, "
                f"{alt.get('duration_min', 0)} menit "
                f"(score: {alt.get('score', 0)})"
            )
    
    return "\n".join(lines)



