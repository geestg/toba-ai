"""Test OpenWeather API key works."""
import requests
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

API_KEY = os.getenv("680bcb2c1eb32b2536522fc2b24a5332")
print("API Key loaded:", bool(API_KEY))

# Test with Danau Toba coordinates (~2.68, 98.71)
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "lat": 2.68,
    "lon": 98.71,
    "appid": API_KEY,
    "units": "metric",
    "lang": "id",
}

try:
    res = requests.get(url, params=params, timeout=10)
    print("Status:", res.status_code)
    data = res.json()
    if res.status_code == 200:
        print("✅ API Key VALID")
        print("Location:", data.get("name"))
        print("Temp:", data["main"]["temp"], "°C")
        print("Condition:", data["weather"][0]["main"], "-", data["weather"][0]["description"])
        print("Humidity:", data["main"]["humidity"], "%")
        print("Wind:", data["wind"]["speed"], "m/s")
    else:
        print("❌ API Error:", data.get("message"))
except Exception as e:
    print("❌ Request failed:", e)

