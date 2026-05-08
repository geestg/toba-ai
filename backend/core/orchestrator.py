from backend.agents.intent_agent import detect_intent

from backend.agents.memory_agent import (
    update_memory,
    get_selected_destination
)

from backend.services.recommendation_service import (
    get_recommendations
)

from backend.core.response_builder import (
    build_response
)

from backend.data_loader import (
    get_destination_by_name,
    get_food_by_destination,
    get_hotels_by_destination,
    get_weather_by_destination,
    get_route_data
)


# =========================================
# MAIN CHAT HANDLER
# =========================================

async def handle_chat(
    message,
    user_id="default_user"
):

    # =====================================
    # DETECT INTENT
    # =====================================

    intent = detect_intent(message)

    update_memory(
        user_id=user_id,
        message=message,
        intent=intent
    )

    # =====================================
    # RECOMMENDATION
    # =====================================

    if intent == "recommendation":

        recommendations = get_recommendations(
            message
        )

        top_destination = recommendations[0]

        update_memory(
            user_id=user_id,
            selected_destination=top_destination
        )

        reply = build_response(
            response_type="recommendation",
            data={
                "message": message,
                "top_destination": top_destination,
                "recommendations": recommendations
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "destinations": recommendations,
                "selected_destination": top_destination
            }
        }

    # =====================================
    # DESTINATION DETAIL
    # =====================================

    elif intent == "destination_detail":

        destination = get_destination_by_name(
            message
        )

        if not destination:

            return {
                "intent": intent,

                "reply": (
                    "Saya belum menemukan informasi destinasi tersebut."
                ),

                "data": {}
            }

        update_memory(
            user_id=user_id,
            selected_destination=destination
        )

        weather = get_weather_by_destination(
            destination["name"]
        )

        reply = build_response(
            response_type="destination_detail",
            data={
                "destination": destination,
                "weather": weather
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "selected_destination": destination,
                "weather": weather
            }
        }

    # =====================================
    # FOOD
    # =====================================

    elif intent == "food":

        destination = get_selected_destination(
            user_id
        )

        if not destination:

            return {
                "intent": intent,

                "reply": (
                    "Pilih destinasi terlebih dahulu sebelum mencari kuliner."
                ),

                "data": {}
            }

        foods = get_food_by_destination(
            destination["name"]
        )

        reply = build_response(
            response_type="food",
            data={
                "destination": destination,
                "foods": foods
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "foods": foods,
                "selected_destination": destination
            }
        }

    # =====================================
    # HOTEL
    # =====================================

    elif intent == "hotel":

        destination = get_selected_destination(
            user_id
        )

        if not destination:

            return {
                "intent": intent,

                "reply": (
                    "Pilih destinasi terlebih dahulu sebelum mencari penginapan."
                ),

                "data": {}
            }

        hotels = get_hotels_by_destination(
            destination["name"]
        )

        reply = build_response(
            response_type="hotel",
            data={
                "destination": destination,
                "hotels": hotels
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "hotels": hotels,
                "selected_destination": destination
            }
        }

    # =====================================
    # ROUTE
    # =====================================

    elif intent == "route":

        destination = get_selected_destination(
            user_id
        )

        if not destination:

            return {
                "intent": intent,

                "reply": (
                    "Pilih destinasi terlebih dahulu sebelum membuat rute."
                ),

                "data": {}
            }

        route = get_route_data(
            destination["name"]
        )

        reply = build_response(
            response_type="route",
            data={
                "destination": destination,
                "route": route
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "route": route,
                "selected_destination": destination
            }
        }

    # =====================================
    # WEATHER
    # =====================================

    elif intent == "weather":

        destination = get_selected_destination(
            user_id
        )

        if not destination:

            return {
                "intent": intent,

                "reply": (
                    "Pilih destinasi terlebih dahulu untuk melihat cuaca."
                ),

                "data": {}
            }

        weather = get_weather_by_destination(
            destination["name"]
        )

        reply = build_response(
            response_type="weather",
            data={
                "destination": destination,
                "weather": weather
            }
        )

        return {
            "intent": intent,

            "reply": reply,

            "data": {
                "weather": weather,
                "selected_destination": destination
            }
        }

    # =====================================
    # FALLBACK
    # =====================================

    return {
        "intent": "unknown",

        "reply": (
            "Saya belum memahami permintaan Anda."
        ),

        "data": {}
    }