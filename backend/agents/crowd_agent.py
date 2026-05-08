import json
from pathlib import Path

# =========================================
# LOAD CROWD DATA
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
CROWD_FILE = BASE_DIR / "data" / "crowd.json"

with open(CROWD_FILE, "r", encoding="utf-8") as f:
    CROWD_DATA = json.load(f)


# =========================================
# ESTIMATE CROWD
# =========================================

def estimate_crowd(destination_name):
    """Get crowd data for a destination."""
    return CROWD_DATA.get(destination_name, {
        "level": "medium",
        "trend": "stabil",
        "best_time": "sekarang"
    })


# =========================================
# SCORE CROWD FOR DESTINATION
# =========================================

def score_crowd_for_destination(destination, crowd):
    """
    Score crowd level (0-1).
    Less crowded (low, quiet) = good for relaxation, etc.
    More crowded (high, busy) = might be fun for some.
    We prefer low to medium for healing, balanced for adventure.
    """
    level = crowd.get("level", "medium").lower()
    
    if level in ["quiet", "rendah", "low", "sepi"]:
        return 0.9
    elif level in ["low_medium", "low-medium"]:
        return 0.8
    elif level in ["medium", "sedang", "ramai"]:
        return 0.6
    elif level in ["high_medium", "high-medium"]:
        return 0.4
    elif level in ["high", "tinggi", "sangat ramai", "very crowded"]:
        return 0.2
    else:
        return 0.5
