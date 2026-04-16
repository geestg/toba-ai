class PolicyAgent:
    def analyze(self, data):
        policies = []

        for loc in data:
            if loc["crowd"] > 75:
                policies.append({
                    "location": loc["name"],
                    "policy": "increase_ticket_price",
                    "value": "+20%"
                })
            elif loc["crowd"] < 40:
                policies.append({
                    "location": loc["name"],
                    "policy": "boost_promotion"
                })

        return policies