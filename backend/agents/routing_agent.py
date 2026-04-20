# routing_agent.py
def run_routing(plan):
    return [{"route": f"Route to {p['name']}", "distance": 10} for p in plan]