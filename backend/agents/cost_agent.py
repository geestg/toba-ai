# cost_agent.py
def run_cost(plan):
    return [{"location": p["name"], "cost": 100000} for p in plan]