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

    # 🔥 CACHE HIT
    cached = get_cache(key)
    if cached:
        return cached

    prompt = f"""
Kamu adalah AI tourism decision system untuk Danau Toba.

User input:
{data.get("user_input")}

Keputusan sistem:
{data.get("chosen")}

Kondisi:
- Cuaca: {data.get("weather")}
- Crowd: {data.get("crowd")}
- UMKM: {data.get("umkm")}
- Impact: {data.get("impact")}
- Plan: {data.get("plan")}
- Booking: {data.get("booking")}

Tugas:
Jelaskan secara natural, singkat, dan meyakinkan kenapa lokasi ini dipilih.
Gunakan bahasa santai tapi tetap profesional.
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
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=10
        )

        if res.status_code != 200:
            print("LLM ERROR:", res.text)
            return fallback_reasoning(data)

        result = res.json()
        output = result["choices"][0]["message"]["content"]

        # SAVE CACHE
        set_cache(key, output)

        return output

    except Exception as e:
        print("LLM EXCEPTION:", str(e))
        return fallback_reasoning(data)


# ========================
# FALLBACK
# ========================
def fallback_reasoning(data):
    chosen = data.get("chosen", {}).get("name", "lokasi ini")

    return f"{chosen} dipilih karena kondisi saat ini paling optimal dibanding alternatif lainnya."