from backend.agents.intent_agent import run_intent
from backend.agents.planner_agent import run_planner
from backend.agents.environment_agent import run_environment
from backend.agents.routing_agent import run_routing
from backend.agents.cost_agent import run_cost
from backend.agents.weather_agent import run_weather
from backend.agents.umkm_agent import run_umkm
from backend.core.decision_engine import make_decision

def process_request(user_input: str):

    intent = run_intent(user_input)

    plan = run_planner(intent)

    environment = run_environment(plan)

    routing = run_routing(plan)

    cost = run_cost(plan)

    weather = run_weather(plan)

    umkm = run_umkm(plan)

    decision = make_decision(
        plan,
        environment,
        routing,
        cost,
        weather,
        umkm
    )

    return {
        "decision": decision,
        "simulation": {
            "before": "crowded",
            "after": "distributed"
        },
        "impact": {
            "environment": "improved",
            "economic": "boosted"
        }
    }