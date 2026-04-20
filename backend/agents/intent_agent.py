def run_intent(user_input):
    text = user_input.lower()

    preferences = {
        "cheap": "murah" in text,
        "quiet": "tidak ramai" in text or "sepi" in text,
        "good_weather": "cuaca bagus" in text or "cerah" in text,
        "relax": "santai" in text
    }

    return {
        "goal": user_input,
        "type": "tourism",
        "preferences": preferences
    }