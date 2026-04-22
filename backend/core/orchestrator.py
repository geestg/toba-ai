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

    # 2. MEMORY
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

        # GUARD: kalau kosong
        if not recs:
            return {
                "intent": intent,
                "reply": "Data destinasi kosong, sistem lagi ga waras.",
                "data": {}
            }

        # 4. PERSONALIZATION
        recs = personalize(recs, memory)

        # GUARD lagi (habis personalize bisa kosong juga)
        if not recs:
            return {
                "intent": intent,
                "reply": "Rekomendasi habis difilter jadi kosong.",
                "data": {}
            }

        # 5. CONTEXT (pakai first item)
        first = recs[0]

        weather = get_weather(first["name"])
        crowd = estimate_crowd(first["name"])

        # 6. DECISION
        best = decide(recs, weather, crowd)

        if not best:
            return {
                "intent": intent,
                "reply": "Ga ada pilihan yang cocok sekarang.",
                "data": {}
            }

        # 7. INSIGHT
        umkm = get_umkm_insight(best, weather)
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

            # FIX TYPE (string vs dict)
            if isinstance(reasoning, dict):
                response["reply"] = reasoning.get("reason", "")
                response["data"]["highlight"] = reasoning.get("highlight")
                response["data"]["summary"] = reasoning.get("summary")
            else:
                response["reply"] = reasoning

        except Exception as e:
            print("LLM ERROR:", e)
            response["reply"] = f"{best['name']} paling cocok saat ini."

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

        try:
            route = get_route(lat, lng, message)

            response["reply"] = "Ini rute paling pas buat perjalanan kau lek."

            response["data"] = {
                "route": route
            }

        except Exception as e:
            print("ROUTE ERROR:", e)
            response["reply"] = "Route error, backend lo lagi ngaco."

    # =========================
    # FALLBACK
    # =========================
    else:
        response["reply"] = "kemana jelasnya lek."

    return response