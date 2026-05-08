from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.core.orchestrator import handle_chat


# =========================================
# FASTAPI INIT
# =========================================

app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================
# REQUEST MODEL
# =========================================

class ChatRequest(BaseModel):

    message: str

    user_id: str = "default_user"


# =========================================
# ROOT
# =========================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "service": "AI Toba Tourism Assistant"
    }


# =========================================
# CHAT ENDPOINT
# =========================================

@app.post("/chat")
async def chat(req: ChatRequest):

    try:

        result = await handle_chat(
            message=req.message,
            user_id=req.user_id
        )

        return result

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return {
            "intent": "error",

            "reply": (
                "Terjadi kesalahan pada sistem."
            ),

            "data": {}
        }