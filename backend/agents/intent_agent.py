def run_intent(user_input: str):
    text = user_input.lower()

    intent = {"type": "general", "preferences": []}

    if "tidak tau" in text or "rekomendasi" in text:
        intent["type"] = "exploration"

    if "santai" in text:
        intent["preferences"].append("relax")

    if "murah" in text:
        intent["preferences"].append("budget")

    if "foto" in text:
        intent["preferences"].append("photo")

    if "alam" in text:
        intent["preferences"].append("nature")

    return intent