from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.chat_engine import process_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(data: dict):
    return process_request(data.get("message"))