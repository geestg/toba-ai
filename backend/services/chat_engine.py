from backend.services.metrics import calculate_distribution

def process_request(user_input):
    data = get_locations()

    decision = orchestrate(user_input, data)

    simulation = simulate(decision)
    impact = calculate_impact(decision)

    distribution_change = calculate_distribution(
        simulation["before"],
        simulation["after"]
    )

    return {
        "decision": decision,
        "simulation": simulation,
        "impact": impact,
        "metrics": {
            "distribution_change": distribution_change
        }
    }