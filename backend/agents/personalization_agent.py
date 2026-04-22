def personalize(recs, user_memory):
    if not isinstance(user_memory, dict):
        return recs  # skip personalization kalau memory kacau

    prefs = user_memory.get("preferences", {})

    # contoh simple: boost nature
    if prefs.get("type") == "nature":
        recs = sorted(recs, key=lambda x: x.get("type") != "nature")

    return recs