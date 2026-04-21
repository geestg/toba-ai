def detect_intent(message: str):
    msg = message.lower()

    if "kemana" in msg or "rekomendasi" in msg:
        return "recommendation"

    if "rute" in msg or "jalan" in msg:
        return "route"

    return "general"