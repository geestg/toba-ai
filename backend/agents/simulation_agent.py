def simulate_impact(destination):
    if destination["rating"] > 4.7:
        return {
            "risk": "Overcrowding tinggi",
            "suggestion": "Alihkan wisatawan ke lokasi alternatif"
        }

    return {
        "risk": "Aman",
        "suggestion": "Cocok untuk distribusi wisata"
    }