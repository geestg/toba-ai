import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

            # VALIDASI
            if isinstance(data, dict):
                return data
            else:
                return {}  # kalau rusak, reset

    except:
        return {}


def save_memory(memory):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def update_memory(user_id, message, location=None):
    memory = load_memory()

    # 🔥 INIT USER
    if user_id not in memory:
        memory[user_id] = {
            "history": [],
            "preferences": {}
        }

    # SAFE GUARD
    if not isinstance(memory[user_id], dict):
        memory[user_id] = {
            "history": [],
            "preferences": {}
        }

    memory[user_id]["history"].append(message)

    if location:
        memory[user_id]["preferences"]["last_location"] = location

    save_memory(memory)

    return memory[user_id]