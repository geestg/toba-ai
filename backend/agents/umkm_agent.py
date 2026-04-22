def get_umkm_insight(location, weather):
    
    if weather["temperature"] > 28:
        return {
            "suggestion": "Minuman dingin & jajanan ringan bakal laris",
            "impact": "UMKM minuman meningkat"
        }
    else:
        return {
            "suggestion": "Makanan hangat lebih diminati",
            "impact": "UMKM kuliner tradisional naik"
        }