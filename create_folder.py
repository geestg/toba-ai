import os

base_path = r"D:\toba-ai\backend"

structure = {
    "": ["app.py"],
    "core": [
        "llm_client.py",
        "orchestrator.py",
        "decision_engine.py",
        "memory.py"
    ],
    "agents": [
        "intent_agent.py",
        "planner_agent.py",
        "routing_agent.py",
        "cost_agent.py",
        "environment_agent.py",
        "umkm_agent.py",
        "weather_agent.py",
        "booking_agent.py",
        "feedback_agent.py"
    ],
    "services": [
        "chat_engine.py",
        "simulation_engine.py",
        "location_service.py",
        "impact_service.py"
    ],
    "data": [
        "locations.json"
    ],
    "utils": [
        "helpers.py"
    ]
}

# create base folder
os.makedirs(base_path, exist_ok=True)

for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    
    # create folder
    os.makedirs(folder_path, exist_ok=True)
    
    # create files
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                if file.endswith(".py"):
                    f.write("# " + file + "\n")
                else:
                    f.write("{}")  # for json placeholder

print("Struktur folder berhasil dibuat. Sekarang tinggal lo isi, jangan cuma jadi pajangan doang.")