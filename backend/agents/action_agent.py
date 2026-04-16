# agents/action_agent.py

class ActionAgent:
    def execute(self, plan, data):
        actions = []

        for step in plan["steps"]:
            if step == "find_hotel":
                actions.append({
                    "type": "booking",
                    "target": "hotel",
                    "status": "reserved (mock)"
                })

            if step == "find_food":
                actions.append({
                    "type": "booking",
                    "target": "restaurant",
                    "status": "reserved (mock)"
                })

            if step == "optimize_route":
                actions.append({
                    "type": "route",
                    "status": "optimized path generated"
                })

        return actions