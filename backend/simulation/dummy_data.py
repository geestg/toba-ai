import random
import os

BASE_PATH = "data"

locations = [
    "Pantai Lumban Bul Bul","Pantai Pakkodian","Huta Meat",
    "Pantai Tambunan","Tara Bunga","Pantai Bebas Parapat",
    "Pantai Pasir Putih Parapat","Batu Gantung",
    "Bukit Indah Simarjarunjung","Tomok","Ambarita",
    "Pantai Parbaba","Bukit Holbung","Aek Rangat",
    "Air Terjun Sipiso Piso","Tongging","Bukit Gajah Bobok",
    "Taman Simalem Resort","Geosite Sipinsur",
    "Huta Ginjang","Lembah Bakkara","Air Terjun Janji"
]

def calculate_crowd():
    base = random.randint(30, 70)
    weekend = random.choice([0, 20])
    weather = random.choice(["sunny", "cloudy", "rainy"])
    weather_effect = 10 if weather == "sunny" else -10 if weather == "rainy" else 0

    score = base + weekend + weather_effect
    return max(0, min(100, score)), weather

def classify(score):
    if score > 75: return "padat"
    if score < 40: return "sepi"
    return "normal"

def get_images(loc):
    folder = os.path.join(BASE_PATH, loc)

    if not os.path.exists(folder):
        return None, []

    files = os.listdir(folder)

    main = None
    gallery = []

    for f in files:
        path = f"/static/{loc}/{f}"
        if "main" in f:
            main = path
        else:
            gallery.append(path)

    return main, gallery


def get_dummy_data():
    data = []

    for loc in locations:
        crowd, weather = calculate_crowd()
        main, gallery = get_images(loc)

        data.append({
            "name": loc,
            "crowd": crowd,
            "status": classify(crowd),
            "weather": weather,
            "image": main,
            "gallery": gallery,
            "description": f"{loc} merupakan destinasi wisata unggulan di Danau Toba."
        })

    return data