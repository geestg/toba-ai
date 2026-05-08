from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio

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
    user_id = payload.get("user_id", "default_user")
    selected_destination = payload.get("selected_destination")
    mobile_data = payload.get("mobile_data")

    result = await handle_chat(
        message,
        lat=lat,
        lng=lng,
        user_id=user_id,
        selected_destination=selected_destination,
        mobile_data=mobile_data
    )
    return result


# STREAMING VERSION
@app.post("/chat-stream")
async def chat_stream(payload: dict):

    async def generate():
        message = payload.get("message", "")
        lat = payload.get("lat")
        lng = payload.get("lng")
        user_id = payload.get("user_id", "default_user")
        selected_destination = payload.get("selected_destination")
        mobile_data = payload.get("mobile_data")

        result = await handle_chat(
            message,
            lat=lat,
            lng=lng,
            user_id=user_id,
            selected_destination=selected_destination,
            mobile_data=mobile_data
        )
        text = result["reply"]

        # streaming per word + delay
        for word in text.split():
            yield word + " "
            await asyncio.sleep(0.03)  # biar keliatan "AI mikir"

    return StreamingResponse(generate(), media_type="text/plain")

