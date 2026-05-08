import json
from pathlib import Path


# =========================================
# LOAD DESTINATIONS
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "destinations.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    DESTINATIONS = json.load(f)


# =========================================
# KEYWORD MAPPING
# =========================================

KEYWORDS = {
    "nature": [
        "alam",
        "nature",
        "healing",
        "view",
        "camping",
        "gunung",
        "pantai",
        "air terjun",
        "relax",
        "sunset"
    ],

    "cultural": [
        "budaya",
        "museum",
        "adat",
        "batak",
        "culture",
        "sejarah",
        "tradisional"
    ],

    "culinary": [
        "makanan",
        "kuliner",
        "food",
        "makan",
        "restoran",
        "cafe"
    ],

    "family": [
        "keluarga",
        "anak",
        "family"
    ],

    "adventure": [
        "tracking",
        "hiking",
        "adventure"
    ]
}


# =========================================
# DETECT USER INTENT
# =========================================

def detect_preferences(user_input: str):
    text = user_input.lower()

    preferences = {
        "types": set(),
        "tags": set(),
        "family": False
    }

    for category, words in KEYWORDS.items():
        for word in words:

            if word in text:

                if category in ["nature", "cultural", "culinary"]:
                    preferences["types"].add(category)

                if category == "family":
                    preferences["family"] = True

                preferences["tags"].add(word)

    return preferences


# =========================================
# SCORE DESTINATION
# =========================================

def calculate_score(destination, preferences):

    score = 0

    # =====================================
    # TYPE MATCH
    # =====================================

    if destination["type"] in preferences["types"]:
        score += 40

    # =====================================
    # TAG MATCH
    # =====================================

    destination_tags = [
        tag.lower()
        for tag in destination.get("tags", [])
    ]

    for tag in preferences["tags"]:
        if tag in destination_tags:
            score += 20

    # =====================================
    # FAMILY FRIENDLY
    # =====================================

    if preferences["family"]:

        if destination.get("family_friendly"):
            score += 15
        else:
            score -= 10

    # =====================================
    # RATING BONUS
    # =====================================

    score += destination.get("rating", 0) * 5

    # =====================================
    # CROWD BONUS
    # =====================================

    crowd = destination.get("crowd")

    if crowd == "low":
        score += 10

    elif crowd == "medium":
        score += 5

    # =====================================
    # WEATHER BONUS
    # =====================================

    weather = destination.get("weather")

    if weather in ["clear", "sunny"]:
        score += 10

    elif weather == "cloudy":
        score += 5

    # =====================================
    # DISTANCE BONUS
    # =====================================

    distance = destination.get("distance", 999)

    if distance <= 10:
        score += 15

    elif distance <= 20:
        score += 10

    elif distance <= 30:
        score += 5

    return round(score, 2)


# =========================================
# MAIN RECOMMENDATION ENGINE
# =========================================

def get_recommendations(user_input: str, limit=5):

    preferences = detect_preferences(user_input)

    scored = []

    for destination in DESTINATIONS:

        score = calculate_score(
            destination,
            preferences
        )

        item = {
            **destination,
            "score": score
        }

        scored.append(item)

    # =====================================
    # SORT DESCENDING
    # =====================================

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # =====================================
    # RETURN TOP RESULTS
    # =====================================

    return scored[:limit]