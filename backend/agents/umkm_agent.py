def get_umkm_insight(location):
    insights = []

    if location["temperature"] > 28:
        insights.append("Cocok buka minuman dingin / es krim")

    if not location.get("has_souvenir"):
        insights.append("Belum ada toko souvenir")

    if not location.get("has_seating"):
        insights.append("Belum ada penyewaan tikar / tempat duduk")

    return insights