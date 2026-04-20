import random
def run_weather(plan):
    return [{"name": l["name"], "weather": random.choice(["sunny","rain"])} for l in plan]