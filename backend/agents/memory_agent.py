import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(user_id, message, location=None):
    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = {
            "history": [],
            "preferences": {}
        }

    memory[user_id]["history"].append(message)

    if location:
        memory[user_id]["last_location"] = location

    save_memory(memory)
    return memory[user_id]

def get_memory(user_id):
    memory = load_memory()
    return memory.get(user_id, {})