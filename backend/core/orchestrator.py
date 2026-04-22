from backend.agents.planner_agent import plan_trip
from backend.agents.booking_agent import simulate_booking

from backend.agents.intent_agent import detect_intent
from backend.agents.recommendation_agent import get_recommendation
from backend.agents.route_agent import get_route
from backend.agents.umkm_agent import get_umkm_insight
from backend.agents.weather_agent import get_weather

from backend.agents.memory_agent import update_memory
from backend.agents.personalization_agent import personalize
from backend.agents.decision_agent import decide
from backend.agents.simulation_agent import simulate_impact
from backend.agents.crowd_agent import estimate_crowd

from backend.core.llm_client import generate_reasoning


async def handle_chat(message, lat, lng, user_id="default_user"):

    # 1. INTENT
    intent = detect_intent(message)

    # 2. MEMORY (SAFE)
    memory = update_memory(user_id, message)

    response = {
        "intent": intent,
        "reply": "",
        "data": {}
    }

    # =========================
    # RECOMMENDATION FLOW
    # =========================
    if intent == "recommendation":

        # 3. RECOMMENDATION
        recs = get_recommendation()

        # 4. PERSONALIZATION
        recs = personalize(recs, memory)

        # 5. CONTEXT
        weather = get_weather(recs[0]["name"])
        crowd = estimate_crowd(recs[0]["name"])

        # 6. DECISION
        best = decide(recs, weather, crowd)

        # 7. INSIGHT
        umkm = get_umkm_insight(best)
        impact = simulate_impact(best)

        # 8. PLAN
        plan = plan_trip(best)

        # 9. BOOKING
        booking = simulate_booking(best)

        # 10. REASONING
        try:
            reasoning = generate_reasoning({
                "user_input": message,
                "chosen": best,
                "weather": weather,
                "crowd": crowd,
                "umkm": umkm,
                "impact": impact,
                "plan": plan,
                "booking": booking
            })

            response["reply"] = reasoning.get("reason", "")

            response["data"].update({
                "highlight": reasoning.get("highlight"),
                "summary": reasoning.get("summary"),
            })

        except Exception as e:
            print("LLM ERROR:", e)
            response["reply"] = f"{best['name']} paling cocok saat ini."

        # JANGAN ADA PARAMETER ANEH
        # update_memory(user_id, message, location=best["name"])

        # kalau mau simpan lokasi, kita upgrade nanti, jangan sekarang bikin error

        # 11. RESPONSE DATA
        response["data"].update({
            "destinations": recs,
            "chosen": best,
            "weather": weather,
            "crowd": crowd,
            "umkm": umkm,
            "impact": impact,
            "plan": plan,
            "booking": booking
        })

    # =========================
    # ROUTE FLOW
    # =========================
    elif intent == "route":

        route = get_route(lat, lng, message)

        response["reply"] = "Ini rute paling pas buat perjalanan kau lek."

        response["data"] = {
            "route": route
        }

    # =========================
    # FALLBACK
    # =========================
    else:
        response["reply"] = "kemana jelasnya lek."

    return response