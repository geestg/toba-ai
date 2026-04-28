import json
import os
from datetime import datetime

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


def update_memory(user_id, message, location=None, selected_destination=None):
    memory = load_memory()

    # INIT USER
    if user_id not in memory:
        memory[user_id] = {
            "history": [],
            "preferences": {},
            "selected_destinations": []
        }

    # SAFE GUARD
    if not isinstance(memory[user_id], dict):
        memory[user_id] = {
            "history": [],
            "preferences": {},
            "selected_destinations": []
        }

    memory[user_id]["history"].append(message)

    if location:
        memory[user_id]["preferences"]["last_location"] = location

    # Save selected destination for follow-up
    if selected_destination and isinstance(selected_destination, dict):
        memory[user_id]["preferences"]["selected_destination"] = selected_destination
        # Also append to history of selected destinations
        if "selected_destinations" not in memory[user_id]:
            memory[user_id]["selected_destinations"] = []
        memory[user_id]["selected_destinations"].append({
            "name": selected_destination.get("name"),
            "timestamp": str(datetime.now()) if 'datetime' in globals() else "now"
        })

    save_memory(memory)

    return memory[user_id]


def get_selected_destination(user_id):
    """Get the currently selected destination for a user."""
    memory = load_memory()
    user_mem = memory.get(user_id, {})
    if isinstance(user_mem, dict):
        return user_mem.get("preferences", {}).get("selected_destination")
    return None


def clear_selected_destination(user_id):
    """Clear the selected destination for a user."""
    memory = load_memory()
    if user_id in memory and isinstance(memory[user_id], dict):
        memory[user_id].get("preferences", {}).pop("selected_destination", None)
        save_memory(memory)

