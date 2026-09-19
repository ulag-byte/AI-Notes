# Ask My Notes

A small AI chatbot that answers questions from your own notes (`notes/*.md`).
The app is kept tiny on purpose; the point is the DevOps around it.

## Roadmap

- [x] 1. App (FastAPI + Ollama locally / Amazon Bedrock on AWS)
- [x] 2. Docker
- [ ] 3. GitHub Actions: lint, build, push to GHCR
- [ ] 4. Kubernetes (kind/minikube): Deployment + Service
- [ ] 5. Terraform: EC2 + security group + IAM role for Bedrock
- [ ] 6. Ansible: user, SSH keys only, firewall, Docker, run container

## Project layout

```
app/main.py      the API (≈70 lines)
app/index.html   a one-page UI
notes/           your cheat sheets (the "knowledge base")
Dockerfile
```

## Configuration (environment variables)

| Variable | Default | Meaning |
| --- | --- | --- |
| `LLM_PROVIDER` | `ollama` | `ollama` or `bedrock` |
| `OLLAMA_URL` | `http://localhost:11434` | Where Ollama runs |
| `OLLAMA_MODEL` | `qwen2.5:3b-instruct` | Any model from `ollama list` |
| `BEDROCK_MODEL_ID` | `amazon.nova-micro-v1:0` | Bedrock model (needs AWS creds + region) |
| `NOTES_DIR` | `notes` | Folder with `.md` notes |

## Step 1: run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000, or:

```powershell
curl.exe -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{\"question\": \"How do I see who uses port 8080?\"}'
```

## Step 2: run in Docker

Start Docker Desktop first.

```powershell
docker build -t ask-my-notes .
docker run --rm -p 8000:8000 -e OLLAMA_URL=http://host.docker.internal:11434 ask-my-notes
```

`host.docker.internal` lets the container reach Ollama running on your laptop.

To use your own notes without rebuilding, mount them:

```powershell
docker run --rm -p 8000:8000 -e OLLAMA_URL=http://host.docker.internal:11434 -v ${PWD}/notes:/app/notes ask-my-notes
```

## Staying at $0

- AWS Budget alert at $1 before creating anything
- `terraform destroy` after every session
- No EKS, no NAT Gateway
- Public GitHub repo (free Actions minutes)
