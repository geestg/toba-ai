def distribution_variance(data):
    values = [d["simulated_crowd"] for d in data]
    mean = sum(values) / len(values)

    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance