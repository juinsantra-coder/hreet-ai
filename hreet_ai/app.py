from __future__ import annotations
import os
from typing import Literal
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
app = FastAPI(title="HREET AI Orange Nexus", version="2.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

SYSTEM_PROMPT = """You are HREET AI, a helpful personal AI assistant.
Answer the user's question directly and accurately. Match the user's language
(Bengali, Hindi, Hinglish, or English). Be clear when you are unsure.
Never claim to have controlled the user's computer, opened files, or performed
an action unless a separately implemented and authorized tool confirms it."""

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=12000)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=24)

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.get("/api/status")
async def status():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
        ready = any(m.get("name", "").split(":")[0] == OLLAMA_MODEL for m in models)
        return {"ok": True, "ollama": "online", "model": OLLAMA_MODEL,
                "model_ready": ready, "models": [m.get("name") for m in models]}
    except (httpx.HTTPError, ValueError):
        return {"ok": True, "ollama": "offline", "model": OLLAMA_MODEL,
                "model_ready": False, "models": []}

@app.post("/api/chat")
async def chat(body: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in body.history[-20:]:
        messages.append({"role": item.role, "content": item.content})
    messages.append({"role": "user", "content": body.message})
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=5.0)) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": OLLAMA_MODEL, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            data = response.json()
        answer = data.get("message", {}).get("content", "").strip()
        if not answer:
            raise HTTPException(status_code=502, detail="The model returned an empty answer.")
        return {"reply": answer, "model": OLLAMA_MODEL}
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Ollama is not running. Start Ollama, then try again.")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="The AI took too long to respond. Try again.")
    except httpx.HTTPStatusError as exc:
        detail = "Model not found. Run: ollama pull " + OLLAMA_MODEL if exc.response.status_code == 404 else "Ollama returned an error."
        raise HTTPException(status_code=502, detail=detail)
