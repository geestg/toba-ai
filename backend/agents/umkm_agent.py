class UMKMAgent:
    def analyze(self, data):
        result = []

        for loc in data:
            if loc["crowd"] < 50:
                result.append({
                    "location": loc["name"],
                    "action": "boost_umkm_visibility"
                })

        return result