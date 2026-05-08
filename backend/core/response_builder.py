import random


# =========================================
# RANDOM OPENERS
# =========================================

RECOMMENDATION_OPENERS = [
    "Kalau ingin suasana yang lebih nyaman sekarang,",
    "Untuk perjalanan saat ini,",
    "Destinasi yang paling cocok sekarang adalah",
    "Berdasarkan kondisi wisata saat ini,"
]

FOOD_OPENERS = [
    "Ada beberapa tempat makan menarik di sekitar lokasi.",
    "Untuk kuliner sekitar,",
    "Kalau ingin cari makanan setelah jalan-jalan,"
]

HOTEL_OPENERS = [
    "Beberapa penginapan yang cukup nyaman di sekitar lokasi adalah",
    "Untuk tempat menginap,",
    "Kalau ingin menginap dekat lokasi,"
]

ROUTE_OPENERS = [
    "Perjalanan menuju lokasi ini cukup nyaman.",
    "Rute menuju destinasi ini relatif lancar.",
    "Untuk perjalanan ke lokasi,"
]


# =========================================
# WEATHER DESCRIPTION
# =========================================

def weather_description(condition):

    mapping = {
        "clear": "cuacanya sedang cerah",
        "sunny": "matahari cukup terang",
        "cloudy": "cuaca agak berawan",
        "foggy": "area sedang berkabut",
        "rainy": "sedang turun hujan ringan"
    }

    return mapping.get(
        condition,
        "cuaca cukup normal"
    )


# =========================================
# CROWD DESCRIPTION
# =========================================

def crowd_description(level):

    mapping = {
        "low": "suasana masih cukup sepi",
        "medium": "pengunjung tidak terlalu padat",
        "high": "area cukup ramai pengunjung"
    }

    return mapping.get(
        level,
        "suasana wisata cukup normal"
    )


# =========================================
# RECOMMENDATION RESPONSE
# =========================================

def build_recommendation(data):

    top = data["top_destination"]

    opener = random.choice(
        RECOMMENDATION_OPENERS
    )

    weather_text = weather_description(
        top.get("weather")
    )

    crowd_text = crowd_description(
        top.get("crowd")
    )

    return (
        f"{opener} {top['name']}. "
        f"Tempat ini cocok untuk dikunjungi karena "
        f"{weather_text} dan {crowd_text}. "
        f"{top.get('description', '')}"
    )


# =========================================
# DESTINATION DETAIL
# =========================================

def build_destination_detail(data):

    destination = data["destination"]

    weather = data["weather"]

    weather_text = weather_description(
        weather.get("condition")
    )

    return (
        f"{destination['name']} merupakan destinasi "
        f"{destination['type']} yang cukup populer di area "
        f"{destination['area']}. "
        f"Saat ini {weather_text} dengan suhu sekitar "
        f"{weather.get('temperature')} derajat."
    )


# =========================================
# FOOD RESPONSE
# =========================================

def build_food(data):

    foods = data["foods"]

    destination = data["destination"]

    if not foods:

        return (
            f"Saya belum menemukan data kuliner "
            f"di sekitar {destination['name']}."
        )

    top_foods = foods[:3]

    names = [
        item["name"]
        for item in top_foods
    ]

    opener = random.choice(
        FOOD_OPENERS
    )

    return (
        f"{opener} "
        f"Beberapa yang cukup populer dekat "
        f"{destination['name']} adalah "
        f"{', '.join(names)}."
    )


# =========================================
# HOTEL RESPONSE
# =========================================

def build_hotel(data):

    hotels = data["hotels"]

    destination = data["destination"]

    if not hotels:

        return (
            f"Saya belum menemukan penginapan "
            f"dekat {destination['name']}."
        )

    names = [
        h["name"]
        for h in hotels[:3]
    ]

    opener = random.choice(
        HOTEL_OPENERS
    )

    return (
        f"{opener} "
        f"{', '.join(names)}."
    )


# =========================================
# ROUTE RESPONSE
# =========================================

def build_route(data):

    route = data["route"]

    destination = data["destination"]

    opener = random.choice(
        ROUTE_OPENERS
    )

    return (
        f"{opener} "
        f"Perjalanan menuju {destination['name']} "
        f"sekitar {route['duration_hours']} jam "
        f"dengan jarak kurang lebih "
        f"{route['distance_km']} kilometer."
    )


# =========================================
# WEATHER RESPONSE
# =========================================

def build_weather(data):

    weather = data["weather"]

    destination = data["destination"]

    weather_text = weather_description(
        weather["condition"]
    )

    return (
        f"Cuaca di {destination['name']} saat ini "
        f"{weather_text} dengan suhu sekitar "
        f"{weather['temperature']} derajat."
    )


# =========================================
# MAIN RESPONSE BUILDER
# =========================================

def build_response(response_type, data):

    if response_type == "recommendation":
        return build_recommendation(data)

    elif response_type == "destination_detail":
        return build_destination_detail(data)

    elif response_type == "food":
        return build_food(data)

    elif response_type == "hotel":
        return build_hotel(data)

    elif response_type == "route":
        return build_route(data)

    elif response_type == "weather":
        return build_weather(data)

    return (
        "Saya siap membantu perjalanan wisata Anda."
    )