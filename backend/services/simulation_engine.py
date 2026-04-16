def simulate_without_ai(data):
    result = []

    for loc in data:
        if "Parapat" in loc["name"] or "Tomok" in loc["name"]:
            loc["simulated_crowd"] = min(100, loc["crowd"] + 20)
        else:
            loc["simulated_crowd"] = max(0, loc["crowd"] - 10)

        result.append(loc)

    return result


def simulate_with_ai(data):
    result = []

    avg = sum([d["crowd"] for d in data]) / len(data)

    for loc in data:
        loc["simulated_crowd"] = int((loc["crowd"] + avg) / 2)
        result.append(loc)

    return result