"""Ask-My-Notes: answer questions using only the markdown notes in NOTES_DIR."""
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" (laptop) or "bedrock" (AWS)
NOTES_DIR = Path(os.getenv("NOTES_DIR", "notes"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")

app = FastAPI(title="Ask My Notes")


class Question(BaseModel):
    question: str


def load_notes() -> str:
    files = sorted(NOTES_DIR.glob("*.md"))
    return "\n\n".join(f"### {f.name}\n{f.read_text(encoding='utf-8')}" for f in files)


def build_prompt(question: str) -> str:
    return (
        "Answer the question using ONLY the notes below. "
        "If the notes don't contain the answer, say so.\n\n"
        f"NOTES:\n{load_notes()}\n\nQUESTION: {question}"
    )


def ask_ollama(prompt: str) -> str:
    r = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": OLLAMA_MODEL, "stream": False, "options": {"num_ctx": 8192},
              "messages": [{"role": "user", "content": prompt}]},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def ask_bedrock(prompt: str) -> str:
    import boto3  # only needed on AWS

    client = boto3.client("bedrock-runtime")
    r = client.converse(modelId=BEDROCK_MODEL,
                        messages=[{"role": "user", "content": [{"text": prompt}]}])
    return r["output"]["message"]["content"][0]["text"]


@app.get("/health")
def health():
    return {"status": "ok", "provider": PROVIDER, "notes": len(list(NOTES_DIR.glob("*.md")))}


@app.post("/ask")
def ask(q: Question):
    ask_llm = ask_bedrock if PROVIDER == "bedrock" else ask_ollama
    try:
        return {"answer": ask_llm(build_prompt(q.question))}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")


@app.get("/", response_class=HTMLResponse)
def home():
    return (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
