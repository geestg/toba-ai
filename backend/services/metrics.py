def calculate_distribution(before, after):
    change = {}

    for loc in before:
        change[loc] = after.get(loc, 0) - before.get(loc, 0)

    return change