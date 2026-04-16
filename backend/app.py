from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from simulation.dummy_data import get_dummy_data
from agents.tourist_agent import TouristAgent
from agents.policy_agent import PolicyAgent
from agents.umkm_agent import UMKMAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 serve static image
app.mount("/static", StaticFiles(directory="data"), name="static")

tourist_agent = TouristAgent()
policy_agent = PolicyAgent()
umkm_agent = UMKMAgent()

@app.get("/decision")
def decision():
    data = get_dummy_data()

    return {
        "data": data,
        "decisions": {
            "tourist": tourist_agent.analyze(data),
            "policy": policy_agent.analyze(data),
            "umkm": umkm_agent.analyze(data)
        }
    }