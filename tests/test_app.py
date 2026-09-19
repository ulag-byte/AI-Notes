from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ask_sends_notes_to_llm(monkeypatch):
    seen = {}

    def fake_llm(prompt):
        seen["prompt"] = prompt
        return "use lsof"

    monkeypatch.setattr(main, "ask_ollama", fake_llm)
    r = client.post("/ask", json={"question": "Who uses port 8080?"})
    assert r.status_code == 200
    assert r.json() == {"answer": "use lsof"}
    assert "lsof -i :8080" in seen["prompt"]  # the notes were included