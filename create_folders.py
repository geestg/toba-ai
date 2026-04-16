import os

BASE_PATH = r"D:\toba-ai\backend\data"

locations = [
    "Pantai Lumban Bul Bul","Pantai Pakkodian","Huta Meat",
    "Pantai Tambunan","Tara Bunga","Pantai Bebas Parapat","Batu Gantung",
    "Bukit Indah Simarjarunjung","Pantai Parbaba","Bukit Holbung","Aek Rangat",
    "Air Terjun Sipiso Piso","Tongging","Bukit Gajah Bobok",
    "Taman Simalem Resort","Geosite Sipinsur",
    "Huta Ginjang","Air Terjun Janji"
]

def create_folders():
    for loc in locations:
        folder_path = os.path.join(BASE_PATH, loc)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"[CREATED] {folder_path}")
        else:
            print(f"[EXISTS]  {folder_path}")

if __name__ == "__main__":
    create_folders()