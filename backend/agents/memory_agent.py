import json
from pathlib import Path


# =========================================
# FILE SETUP
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "data" / "users.json"


# =========================================
# LOAD MEMORY
# =========================================

def load_memory():

    if not MEMORY_FILE.exists():

        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================================
# SAVE MEMORY
# =========================================

def save_memory(data):

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# =========================================
# FIND USER
# =========================================

def find_user(memory, user_id):

    for user in memory:

        if user["user_id"] == user_id:
            return user

    return None


# =========================================
# CREATE USER
# =========================================

def create_user(user_id):

    memory = load_memory()

    new_user = {
        "user_id": user_id,

        "selected_destination": None,

        "last_intent": None,

        "conversation_history": []
    }

    memory.append(new_user)

    save_memory(memory)

    return new_user


# =========================================
# GET USER MEMORY
# =========================================

def get_user_memory(user_id):

    memory = load_memory()

    user = find_user(memory, user_id)

    if not user:
        user = create_user(user_id)

    return user


# =========================================
# UPDATE MEMORY
# =========================================

def update_memory(
    user_id,
    message=None,
    intent=None,
    selected_destination=None
):

    memory = load_memory()

    user = find_user(memory, user_id)

    if not user:

        user = {
            "user_id": user_id,

            "selected_destination": None,

            "last_intent": None,

            "conversation_history": []
        }

        memory.append(user)

    # =====================================
    # UPDATE DESTINATION
    # =====================================

    if selected_destination:

        user["selected_destination"] = {
            "id": selected_destination.get("id"),
            "name": selected_destination.get("name"),
            "type": selected_destination.get("type"),
            "area": selected_destination.get("area")
        }

    # =====================================
    # UPDATE INTENT
    # =====================================

    if intent:
        user["last_intent"] = intent

    # =====================================
    # SAVE CHAT HISTORY
    # =====================================

    if message:

        user["conversation_history"].append(message)

        # LIMIT HISTORY
        user["conversation_history"] = (
            user["conversation_history"][-10:]
        )

    save_memory(memory)

    return user


# =========================================
# GET SELECTED DESTINATION
# =========================================

def get_selected_destination(user_id):

    user = get_user_memory(user_id)

    return user.get("selected_destination")


# =========================================
# GET LAST INTENT
# =========================================

def get_last_intent(user_id):

    user = get_user_memory(user_id)

    return user.get("last_intent")


# =========================================
# CLEAR MEMORY
# =========================================

def clear_memory(user_id):

    memory = load_memory()

    filtered = []

    for user in memory:

        if user["user_id"] != user_id:
            filtered.append(user)

    save_memory(filtered)