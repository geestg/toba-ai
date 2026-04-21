from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.orchestrator import handle_chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Toba AI Backend Running"}

@app.post("/chat")
async def chat(payload: dict):
    message = payload.get("message", "")
    lat = payload.get("lat")
    lng = payload.get("lng")

    result = await handle_chat(message, lat, lng)
    return result