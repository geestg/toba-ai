# backend/agents/planner_agent.py

def plan_trip(destination):
    if not destination:
        return {
            "error": "Destinasi kosong, ga bisa bikin plan"
        }

    name = destination.get("name", "Unknown")

    return {
        "day_1": f"Berangkat ke {name} + eksplor area utama",
        "day_2": f"Explore spot populer di {name}",
        "day_3": "Kuliner lokal + persiapan pulang"
    }