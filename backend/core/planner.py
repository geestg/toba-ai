# core/planner.py

class TaskPlanner:
    def create_plan(self, user_input):
        plan = {
            "goal": user_input,
            "steps": []
        }

        if "hotel" in user_input or "menginap" in user_input:
            plan["steps"].append("find_hotel")

        if "makan" in user_input:
            plan["steps"].append("find_food")

        plan["steps"].append("optimize_route")
        plan["steps"].append("distribute_crowd")

        return plan