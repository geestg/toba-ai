# app.py
from fastapi import FastAPI
from backend.services.chat_engine import process_request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Toba AI Running"}

@app.post("/chat")
def chat(request: dict):
    user_input = request.get("message")
    result = process_request(user_input)
    return result