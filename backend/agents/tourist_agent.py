class TouristAgent:
    def analyze(self, data):
        decisions = []

        for loc in data:
            if loc["crowd"] > 75:
                alt = self.find_alternative(data)

                decisions.append({
                    "from": loc["name"],
                    "to": alt["name"],
                    "action": "redirect",
                    "reason": f"Kepadatan tinggi ({loc['crowd']})"
                })

        return decisions

    def find_alternative(self, data):
        sorted_data = sorted(data, key=lambda x: x["crowd"])
        return sorted_data[0]