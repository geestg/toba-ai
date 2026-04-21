from backend.agents.intent_agent import detect_intent
from backend.agents.recommendation_agent import get_recommendation
from backend.agents.route_agent import get_route
from backend.agents.umkm_agent import get_umkm_insight
from backend.agents.weather_agent import get_weather

from backend.agents.memory_agent import update_memory, get_memory
from backend.agents.personalization_agent import personalize
from backend.agents.decision_agent import decide
from backend.agents.simulation_agent import simulate_impact
from backend.agents.crowd_agent import estimate_crowd

from backend.core.llm_client import generate_reasoning


async def handle_chat(message, lat, lng, user_id="default_user"):
    # 1. DETECT INTENT
    intent = detect_intent(message)

    # 2. UPDATE MEMORY
    memory = update_memory(user_id, message)

    response = {
        "intent": intent,
        "reply": "",
        "data": {}
    }

    # =========================
    # FLOW
    # =========================
    if intent == "recommendation":

        # 3. GET DATA
        recs = get_recommendation()

        # 4. PERSONALIZATION
        recs = personalize(recs, memory)

        # 5. CONTEXT ANALYSIS
        weather = get_weather(recs[0]["name"])
        crowd = estimate_crowd(recs[0]["name"])

        # 6. DECISION ENGINE
        best = decide(recs, weather, crowd)

        # 7. EXTRA INSIGHT
        umkm = get_umkm_insight(best)
        impact = simulate_impact(best)

        # 8. GPT REASONING 
        try:
            reasoning = generate_reasoning({
                "user_input": message,
                "chosen": best,
                "weather": weather,
                "crowd": crowd,
                "umkm": umkm,
                "impact": impact
            })
        except Exception as e:
            # fallback kalau API error
            reasoning = f"{best['name']} paling cocok karena kondisi lebih optimal saat ini."

        # 9. SAVE MEMORY (OPTIONAL IMPROVE)
        update_memory(user_id, message, location=best["name"])

        # 10. FINAL RESPONSE
        response["reply"] = reasoning

        response["data"] = {
            "destinations": recs,
            "chosen": best,
            "weather": weather,
            "crowd": crowd,
            "umkm": umkm,
            "impact": impact
        }

    # =========================
    # ROUTE FLOW
    # =========================
    elif intent == "route":

        route = get_route(lat, lng, message)

        response["reply"] = "Ini rute paling masuk akal buat perjalanan kau."

        response["data"] = {
            "route": route
        }

    # =========================
    # FALLBACK
    # =========================
    else:
        response["reply"] = "Jelaskan tujuan kau dengan jelas, jangan bikin sistem mikir sendiri."

    return response