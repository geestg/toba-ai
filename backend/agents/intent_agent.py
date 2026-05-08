# =========================================
# INTENT KEYWORDS
# =========================================

INTENT_PATTERNS = {

    "recommendation": [
        "rekomendasi",
        "wisata",
        "healing",
        "liburan",
        "jalan jalan",
        "refreshing",
        "destinasi",
        "camping",
        "pantai",
        "alam",
        "view",
        "sunset",
        "culture",
        "budaya",
        "museum",
        "adat"
    ],

    "route": [
        "rute",
        "route",
        "jalan",
        "arah",
        "perjalanan",
        "cara pergi",
        "lokasi",
        "map"
    ],

    "food": [
        "makan",
        "kuliner",
        "makanan",
        "restoran",
        "cafe",
        "rumah makan",
        "tempat makan"
    ],

    "hotel": [
        "hotel",
        "penginapan",
        "homestay",
        "villa",
        "resort",
        "tempat tinggal"
    ],

    "itinerary": [
        "itinerary",
        "jadwal",
        "rencana perjalanan",
        "trip plan",
        "3 hari",
        "2 hari",
        "planning"
    ],

    "weather": [
        "cuaca",
        "hujan",
        "panas",
        "dingin",
        "kabut"
    ],

    "crowd": [
        "ramai",
        "crowd",
        "sepi",
        "padat"
    ]
}


# =========================================
# DESTINATION DETECTOR
# =========================================

KNOWN_DESTINATIONS = [
    "sibea bea",
    "bukit holbung",
    "pantai parbaba",
    "museum huta bolon",
    "desa tomok",
    "sipiso piso",
    "taman eden",
    "batu gantung"
]


# =========================================
# DETECT INTENT
# =========================================

def detect_intent(user_input: str):

    text = user_input.lower()

    # =====================================
    # PRIORITY INTENT
    # =====================================

    # FOOD
    for word in INTENT_PATTERNS["food"]:
        if word in text:
            return "food"

    # HOTEL
    for word in INTENT_PATTERNS["hotel"]:
        if word in text:
            return "hotel"

    # ROUTE
    for word in INTENT_PATTERNS["route"]:
        if word in text:
            return "route"

    # ITINERARY
    for word in INTENT_PATTERNS["itinerary"]:
        if word in text:
            return "itinerary"

    # WEATHER
    for word in INTENT_PATTERNS["weather"]:
        if word in text:
            return "weather"

    # CROWD
    for word in INTENT_PATTERNS["crowd"]:
        if word in text:
            return "crowd"

    # =====================================
    # DESTINATION NAME DETECTION
    # =====================================

    for destination in KNOWN_DESTINATIONS:

        if destination in text:
            return "destination_detail"

    # =====================================
    # DEFAULT RECOMMENDATION
    # =====================================

    return "recommendation"