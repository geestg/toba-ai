def detect_intent(message: str):
    msg = message.lower().strip()

    # Recommendation intents
    if any(k in msg for k in ["kemana", "rekomendasi", "destinasi", "tempat", "wisata", "liburan", "jalan-jalan"]):
        return "recommendation"

    # Select destination intent
    if any(k in msg for k in ["pilih", "select", "mau ke", "ke sana", "ke situ", "yang ini", "yang itu"]):
        return "select_destination"

    # Route intents
    if any(k in msg for k in ["rute", "jalan", "arah", "menuju", "cara ke", "bagaimana ke"]):
        return "route"

    # Nearby food / UMKM
    if any(k in msg for k in ["makan", "makanan", "restoran", "rumah makan", "kuliner", "jajanan", "umkm", "food", "cafe"]):
        return "nearby_food"

    # Nearby hotel / accommodation
    if any(k in msg for k in ["hotel", "penginapan", "homestay", "inap", "tidur", "menginap", "booking"]):
        return "nearby_hotel"

    # Itinerary / plan
    if any(k in msg for k in ["itinerary", "rencana", "plan", "jadwal", "hari", "trip plan"]):
        return "itinerary"

    return "general"

