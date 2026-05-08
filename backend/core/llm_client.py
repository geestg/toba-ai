import requests
import os
import json
import hashlib
import time
from dotenv import load_dotenv

# ========================
# LOAD ENV
# ========================
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

URL = "https://api.openai.com/v1/chat/completions"

# ========================
# CACHE CONFIG
# ========================
cache = {}
CACHE_TTL = 300  # 5 menit


# ========================
# SYSTEM PROMPT
# ========================
SYSTEM_PROMPT = """
Kamu adalah AI travel assistant Danau Toba bernama AI Toba.

Kepribadian:
- Friendly
- Santai
- Natural
- Tidak terlalu formal
- Tidak kaku
- Seperti guide wisata lokal modern
- Ringkas tapi membantu
- Hangat dan komunikatif

Aturan menjawab:
- Gunakan bahasa Indonesia natural
- Hindari jawaban seperti laporan sistem
- Jangan terlalu banyak data mentah
- Jangan terlalu panjang
- Fokus membantu user mengambil keputusan wisata
- Jelaskan alasan rekomendasi dengan sederhana
- Gunakan gaya ngobrol yang enak dibaca

Contoh gaya jawaban yang benar:
"Tempat ini lagi cukup nyaman dikunjungi karena cuacanya bagus dan belum terlalu ramai."

"Kalau kamu suka suasana tenang sambil lihat budaya Batak, tempat ini cocok banget."

"Perjalanan ke sana sekitar 2 jam dan view jalannya juga bagus."
"""


# ========================
# CACHE UTILS
# ========================
def get_cache(key):
    if key in cache:
        value, timestamp = cache[key]

        # cek expired
        if time.time() - timestamp < CACHE_TTL:
            return value
        else:
            del cache[key]

    return None


def set_cache(key, value):
    cache[key] = (value, time.time())


# ========================
# CACHE KEY GENERATOR
# ========================
def generate_cache_key(data):
    normalized = json.dumps(data, sort_keys=True)
    return hashlib.md5(normalized.encode()).hexdigest()


# ========================
# MAIN LLM FUNCTION
# ========================
def generate_reasoning(data):

    key = generate_cache_key(data)

    # ========================
    # CACHE HIT
    # ========================
    cached = get_cache(key)

    if cached:
        return cached

    # ========================
    # BUILD PROMPT
    # ========================
    prompt = f"""
User bertanya:
{data.get("user_input")}

Lokasi yang dipilih:
{data.get("chosen")}

Kondisi saat ini:
- Cuaca: {data.get("weather")}
- Crowd: {data.get("crowd")}
- UMKM: {data.get("umkm")}
- Impact: {data.get("impact")}
- Plan: {data.get("plan")}
- Booking: {data.get("booking")}

Tugas:
Berikan penjelasan singkat dan natural kenapa lokasi ini cocok untuk user.
Buat terasa seperti AI assistant wisata yang ramah dan membantu.
"""

    try:

        res = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8,
                "max_tokens": 180
            },
            timeout=15
        )

        # ========================
        # ERROR API
        # ========================
        if res.status_code != 200:
            print("LLM ERROR:", res.text)
            return fallback_reasoning(data)

        result = res.json()

        output = result["choices"][0]["message"]["content"].strip()

        # ========================
        # SAVE CACHE
        # ========================
        set_cache(key, output)

        return output

    except Exception as e:

        print("LLM EXCEPTION:", str(e))

        return fallback_reasoning(data)


# ========================
# FALLBACK RESPONSE
# ========================
def fallback_reasoning(data):

    chosen = data.get("chosen", {})

    if isinstance(chosen, dict):
        name = chosen.get("name", "destinasi ini")
    else:
        name = str(chosen)

    return (
        f"{name} lagi cukup bagus dikunjungi sekarang karena suasananya nyaman "
        f"dan cocok buat perjalanan santai di sekitar Danau Toba."
    )