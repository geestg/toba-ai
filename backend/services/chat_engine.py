from backend.agents.intent_agent import run_intent
from backend.agents.planner_agent import run_planner
from backend.agents.environment_agent import run_environment
from backend.agents.routing_agent import run_routing
from backend.agents.cost_agent import run_cost
from backend.agents.weather_agent import run_weather
from backend.agents.umkm_agent import run_umkm
from backend.agents.booking_agent import run_booking

from backend.core.decision_engine import make_decision
from backend.services.impact_service import calculate_impact


def process_request(user_input):

    intent = run_intent(user_input)

    plan = run_planner(intent)

    environment = run_environment(plan)

    routing = run_routing(plan)

    cost = run_cost(plan)

    weather = run_weather(plan)

    umkm = run_umkm(plan)

    decision = make_decision(intent, environment, routing, cost, weather, umkm)

    loc = decision["final_decision"]

    return {
        "decision": decision,
        "supporting": {
            "food": loc["food"],
            "stay": loc["stay"]
        },
        "impact": calculate_impact(loc),
        "agent_trace": {
            "intent": intent,
            "top_choice": loc["name"]
        }
    }