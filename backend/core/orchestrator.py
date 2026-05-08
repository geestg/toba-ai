from backend.agents.planner_agent import plan_trip
from backend.agents.booking_agent import simulate_booking, find_nearby_hotels

from backend.agents.intent_agent import detect_intent
from backend.agents.recommendation_agent import get_recommendation
from backend.agents.route_agent import get_route
from backend.agents.umkm_agent import get_umkm_insight, find_nearby_umkm
from backend.agents.weather_agent import get_weather

from backend.agents.memory_agent import update_memory, get_selected_destination
from backend.agents.personalization_agent import personalize
from backend.agents.decision_agent import decide
from backend.agents.simulation_agent import simulate_impact
from backend.agents.crowd_agent import estimate_crowd

from backend.core.llm_client import generate_reasoning
from backend.services.location_service import get_locations


def _wants_nearby(message):
    """Detect if user is explicitly asking for nearby places."""
    msg_lower = message.lower()
    nearby_keywords = [
        "sekitar", "terdekat", "dekat", "nearby", "near",
        "sekitar saya", "dekat sini", "dekat saya",
        "terdekat dari", "paling dekat", "closest"
    ]
    return any(kw in msg_lower for kw in nearby_keywords)


def _find_destination_by_name(name):
    """Find a destination by name from the locations database."""
    locations = get_locations()
    name_lower = name.lower()
    for loc in locations:
        if loc["name"].lower() == name_lower:
            return loc
    return None


async def handle_chat(message, lat=None, lng=None, user_id="default_user", selected_destination=None, mobile_data=None):

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

        # Only consider distance if user explicitly asks for nearby places
        consider_distance = _wants_nearby(message)
        scored_recs = get_recommendation(
            user_lat=lat, user_lng=lng,
            consider_distance=consider_distance,
            top_n=5
        )

        # GUARD: kalau kosong
        if not scored_recs:
            return {
                "intent": intent,
                "reply": "Maaf, tidak ada destinasi yang tersedia saat ini.",
                "data": {}
            }

        # Build ranked list with explanations
        ranked = decide(scored_recs)

        # Build natural language reply
        top = ranked[0]
        reply_lines = [
            f"Berikut top {len(ranked)} rekomendasi destinasi untuk Anda:",
            ""
        ]

        for i, dest in enumerate(ranked, 1):
            reply_lines.append(
                f"{i}. **{dest['name']}** (Score: {dest['score']})")
            reply_lines.append(f"   {dest['reason']}")
            reply_lines.append(f"   🌤️ {dest['weather_note']}")
            reply_lines.append(f"   👥 {dest['crowd_note']}")
            reply_lines.append("")

        reply_lines.append(f"Destinasi teratas: **{top['name']}**. Klik 'Pilih' untuk melanjutkan.")

        response["reply"] = "\n".join(reply_lines)
        response["data"] = {
            "destinations": ranked,
            "top_destination": top
        }

    # =========================
    # SELECT DESTINATION FLOW
    # =========================
    elif intent == "select_destination":
        # Try to extract destination name from message
        # Common patterns: "pilih Holbung", "mau ke Holbung", "yang ini", etc.
        dest_name = None

        if selected_destination and isinstance(selected_destination, dict):
            dest_name = selected_destination.get("name")
        else:
            # Try to find destination name in message
            locations = get_locations()
            msg_lower = message.lower()
            for loc in locations:
                if loc["name"].lower() in msg_lower:
                    dest_name = loc["name"]
                    selected_destination = loc
                    break

        if not dest_name or not selected_destination:
            response["reply"] = "Maaf, saya tidak tahu destinasi mana yang Anda maksud. Silakan pilih dari daftar rekomendasi."
            return response

        # Save to memory
        update_memory(user_id, message, selected_destination=selected_destination)

        # Get weather and crowd for the selected destination
        weather = get_weather(dest_name, selected_destination.get("area"))
        crowd = estimate_crowd(dest_name, selected_destination.get("baseline_crowd", 0.5))

        response["reply"] = (
            f"✅ **{dest_name}** dipilih!\n\n"
            f"🌤️ Cuaca: {weather['condition']}, {weather['temperature']}°C\n"
            f"👥 Keramaian: {crowd['level']} (trend: {crowd['trend']})\n\n"
            f"Mau saya buatkan rute? Atau cari rumah makan/penginapan sekitar?"
        )
        response["data"] = {
            "selected_destination": selected_destination,
            "weather": weather,
            "crowd": crowd
        }

    # =========================
    # ROUTE FLOW (SMART ROUTING)
    # =========================
    elif intent == "route":
        # Check if user has a selected destination in memory
        saved_dest = get_selected_destination(user_id)

        end_coords = None
        end_name = None
        end_area = None

        if saved_dest:
            end_coords = {
                "lat": saved_dest.get("lat"),
                "lng": saved_dest.get("lng")
            }
            end_name = saved_dest.get("name")
            end_area = saved_dest.get("area")

        # If no saved destination, try to parse from message
        if not end_coords:
            locations = get_locations()
            msg_lower = message.lower()
            for loc in locations:
                if loc["name"].lower() in msg_lower:
                    end_coords = {"lat": loc["lat"], "lng": loc["lng"]}
                    end_name = loc["name"]
                    end_area = loc.get("area")
                    break

        if not end_coords:
            response["reply"] = "Maaf, saya tidak tahu tujuan Anda. Silakan pilih destinasi terlebih dahulu."
            return response

        # Use user location as start if available
        start_lat = lat if lat is not None else 2.684
        start_lng = lng if lng is not None else 98.875

        try:
            route_data = get_route(start_lat, start_lng, end_name or "destinasi", end_area)
            
            response["reply"] = route_data.get("explanation", "Rute berhasil dibuat.")
            response["data"] = {
                "route": route_data.get("segments") or route_data.get("best", {}).get("path"),
                "start": {"lat": start_lat, "lng": start_lng},
                "end": end_coords,
                "destination_name": end_name,
                "total_distance_km": route_data.get("total_distance_km") or route_data.get("best", {}).get("distance_km"),
                "total_duration_min": route_data.get("total_duration_min") or route_data.get("best", {}).get("duration_min"),
            }

        except Exception as e:
            print("ROUTE ERROR:", e)
            response["reply"] = "Maaf, gagal membuat rute. Coba lagi nanti."

    # =========================
    # NEARBY FOOD / UMKM FLOW
    # =========================
    elif intent == "nearby_food":
        saved_dest = get_selected_destination(user_id)

        if not saved_dest:
            response["reply"] = "Silakan pilih destinasi terlebih dahulu agar saya bisa mencari rumah makan di sekitarnya."
            return response

        # Get UMKM insight and nearby UMKM list
        weather = get_weather(saved_dest["name"], saved_dest.get("area"))
        umkm_insight = get_umkm_insight(saved_dest["name"], weather, selected_destination=saved_dest)
        nearby_umkm = find_nearby_umkm(saved_dest)

        reply_lines = [
            f"🍽️ Rekomendasi kuliner sekitar **{saved_dest['name']}**:",
            ""
        ]

        if nearby_umkm.get("umkm_list"):
            for i, place in enumerate(nearby_umkm["umkm_list"][:5], 1):
                reply_lines.append(
                    f"{i}. **{place['name']}** ({place['type']})\n"
                    f"   ⭐ {place['rating']} | 📍 {place['distance_km']} km"
                )

        reply_lines.append("")
        reply_lines.append(f"💡 {umkm_insight['suggestion']}")

        response["reply"] = "\n".join(reply_lines)
        response["data"] = {
            "selected_destination": saved_dest,
            "umkm_insight": umkm_insight,
            "nearby_umkm": nearby_umkm
        }

    # =========================
    # NEARBY HOTEL FLOW
    # =========================
    elif intent == "nearby_hotel":
        saved_dest = get_selected_destination(user_id)

        if not saved_dest:
            response["reply"] = "Silakan pilih destinasi terlebih dahulu agar saya bisa mencari penginapan di sekitarnya."
            return response

        hotels = find_nearby_hotels(saved_dest)

        reply_lines = [
            f"🏨 Rekomendasi penginapan sekitar **{saved_dest['name']}**:",
            ""
        ]

        if hotels.get("hotels"):
            for i, hotel in enumerate(hotels["hotels"][:5], 1):
                reply_lines.append(
                    f"{i}. **{hotel['name']}** ({hotel['type']})\n"
                    f"   ⭐ {hotel['rating']} | 💰 {hotel['price']} | 📍 {hotel['distance_km']} km"
                )

        reply_lines.append("")
        reply_lines.append(f"Tersedia {hotels.get('count', 0)} pilihan penginapan di area {hotels.get('area', 'ini')}.")

        response["reply"] = "\n".join(reply_lines)
        response["data"] = {
            "selected_destination": saved_dest,
            "hotels": hotels
        }

    # =========================
    # ITINERARY FLOW
    # =========================
    elif intent == "itinerary":
        saved_dest = get_selected_destination(user_id)
        target = saved_dest if saved_dest else {"name": "Danau Toba"}

        plan = plan_trip(target)

        reply_lines = [
            f"📅 Rencana perjalanan ke **{target.get('name', 'Danau Toba')}**:",
            ""
        ]

        for day, activity in plan.items():
            reply_lines.append(f"**{day.replace('_', ' ').title()}:** {activity}")

        response["reply"] = "\n".join(reply_lines)
        response["data"] = {
            "plan": plan,
            "destination": target
        }

    # =========================
    # FALLBACK
    # =========================
    else:
        response["reply"] = "Maaf, saya tidak mengerti. Coba tanyakan tentang rekomendasi destinasi, rute, rumah makan, atau penginapan."

    return response

