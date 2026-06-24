from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_MODEL = "llama-3.1-8b-instant"

class ChatRequest(BaseModel):
    messages: list
    mode: str = "Chat"

@app.post("/api/chat")
def chat(req: ChatRequest):
    api_key = os.environ["GROQ_API_KEY"]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": req.messages,
            "temperature": 0.7,
            "max_tokens": 900
        },
        timeout=60
    )
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"]
    return {"reply": reply}

@app.get("/api/health")
def health():
    return {"status": "ok"}
