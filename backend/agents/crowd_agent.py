from datetime import datetime


def estimate_crowd(location_name, baseline_crowd=0.5, mobile_data=None):
    """
    Estimate crowd level for a location and return a numeric score (0-1).

    Supports multiple data sources:
    1. Baseline crowd (from location metadata)
    2. Time-based heuristics (hour, weekday/weekend)
    3. Mobile/GPS data (optional, from app users, Wi-Fi, or operator data)

    Args:
        location_name: Name of the destination
        baseline_crowd: Base crowd level for the location (0-1, from location metadata)
        mobile_data: Optional dict with mobile/GPS crowd signals, e.g.:
            {
                "device_count": 120,          # Number of devices detected in area
                "max_capacity": 500,          # Estimated max capacity
                "mobility_index": 0.6,        # Normalized mobility score (0-1)
                "data_source": "app_gps",     # "app_gps", "wifi", "operator", "google_mobility"
                "sample_size": 45,            # Percentage of total visitors sampled
                "timestamp": "2024-01-15T14:30:00"
            }

    Returns:
        dict with crowd score (0-1), level label, trend, best_time, and data_source_note
    """
    hour = datetime.now().hour
    day = datetime.now().weekday()  # 0=Monday, 6=Sunday

    # ===== TIME-BASED HEURISTICS =====
    if 6 <= hour < 9:
        time_mult = 0.3
    elif 9 <= hour < 12:
        time_mult = 0.7
    elif 12 <= hour < 15:
        time_mult = 1.0
    elif 15 <= hour < 18:
        time_mult = 0.85
    elif 18 <= hour < 21:
        time_mult = 0.6
    else:
        time_mult = 0.2

    weekend_mult = 1.3 if day >= 5 else 1.0
    # Deterministic fluctuation based on location + hour (no random)
    fluctuation = ((hash(location_name) % 21) - 10) / 100.0  # -0.10 to +0.10

    heuristic_score = baseline_crowd * time_mult * weekend_mult + fluctuation
    heuristic_score = max(0.0, min(1.0, heuristic_score))

    # ===== MOBILE/GPS DATA (if available) =====
    mobile_score = None
    data_source_note = "Estimasi berdasarkan waktu & baseline"
    confidence = "medium"

    if mobile_data and isinstance(mobile_data, dict):
        device_count = mobile_data.get("device_count")
        max_capacity = mobile_data.get("max_capacity")
        mobility_index = mobile_data.get("mobility_index")
        sample_size = mobile_data.get("sample_size", 100)
        source = mobile_data.get("data_source", "unknown")

        # Calculate mobile-based crowd score
        if device_count is not None and max_capacity is not None and max_capacity > 0:
            mobile_score = device_count / max_capacity
            mobile_score = max(0.0, min(1.0, mobile_score))
        elif mobility_index is not None:
            mobile_score = max(0.0, min(1.0, mobility_index))

        # Adjust for sample size (lower sample = less confident, blend more toward heuristic)
        sample_weight = min(sample_size / 100.0, 1.0) if sample_size else 0.5

        if mobile_score is not None:
            # Blend mobile data with heuristic based on sample size
            # Higher sample size = trust mobile data more
            mobile_weight = 0.4 + (sample_weight * 0.4)  # 0.4 to 0.8
            heuristic_weight = 1.0 - mobile_weight

            crowd_score = mobile_score * mobile_weight + heuristic_score * heuristic_weight
            crowd_score = max(0.0, min(1.0, crowd_score))

            confidence = "high" if sample_weight > 0.7 else "medium"
            data_source_note = (
                f"Data crowd dari {source} ({sample_size}% sampel) "
                f"digabung dengan estimasi waktu"
            )
        else:
            crowd_score = heuristic_score
    else:
        crowd_score = heuristic_score

    # ===== DETERMINE LEVEL LABEL =====
    if crowd_score >= 0.7:
        level = "ramai"
    elif crowd_score >= 0.4:
        level = "sedang"
    else:
        level = "sepi"

    # ===== TREND =====
    if mobile_data and "trend" in mobile_data:
        trend = mobile_data["trend"]
    elif hour < 12:
        trend = "naik"
    elif hour < 16:
        trend = "stabil"
    else:
        trend = "turun"

    # ===== BEST TIME RECOMMENDATION =====
    if level == "ramai":
        best_time = "pagi hari (sebelum jam 9)"
    elif level == "sedang":
        best_time = "sekarang atau sore hari"
    else:
        best_time = "sekarang"

    return {
        "location": location_name,
        "score": round(crowd_score, 2),
        "level": level,
        "trend": trend,
        "best_time": best_time,
        "confidence": confidence,
        "data_source_note": data_source_note,
        "heuristic_score": round(heuristic_score, 2),
        "mobile_score": round(mobile_score, 2) if mobile_score is not None else None,
        "sample_size": mobile_data.get("sample_size") if mobile_data else None
    }

