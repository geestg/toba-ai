# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.chat_engine import process_user_query
from simulation.dummy_data import get_dummy_data
from services.simulation_engine import simulate_with_ai, simulate_without_ai
from services.metrics import distribution_variance
from services.explanation_engine import generate_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(payload: dict):
    query = payload.get("message", "")

    result = process_user_query(query)

    return result


@app.get("/simulate")
def simulate():
    data = get_dummy_data()

    before = simulate_without_ai([d.copy() for d in data])
    after = simulate_with_ai([d.copy() for d in data])

    before_var = distribution_variance(before)
    after_var = distribution_variance(after)

    return {
        "impact": round(before_var - after_var, 2),
        "summary": generate_summary(before_var, after_var),
        "before": before,
        "after": after,
    }