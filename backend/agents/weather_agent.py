# weather_agent.py
import random

def run_weather(plan):
    return [{"location": p["name"], "weather": random.choice(["sunny", "rain"])} for p in plan]