# environment_agent.py
def run_environment(plan):
    for loc in plan:
        loc["sustainability_score"] = 100 - loc["crowd"]
    return plan