import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

URL = "https://api.openai.com/v1/chat/completions"


def generate_reasoning(data):
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

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM EXCEPTION:", str(e))
        return fallback_reasoning(data)


def fallback_reasoning(data):
    chosen = data.get("chosen", {}).get("name", "lokasi ini")

    return f"{chosen} dipilih karena kondisi saat ini paling optimal dibanding alternatif lainnya."