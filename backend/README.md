# Backend - AI Interview Agent

FastAPI backend application powering the AI Interview Agent system.

## Modules Structure
- `app/main.py`: Entry point and FastAPI application setup
- `app/routes/`: API endpoint definitions (`POST /api/interview`)
- `app/services/`: Personalization, Interview Engine, and LLM Provider service
- `app/models/`: Pydantic models for Candidate, Session, Request, and Response payloads
- `app/prompts/`: Dynamic prompt generators for technical interview personas
- `app/session/`: In-memory session manager maintaining state by `sessionId`
- `data/`: Cohort curriculum and candidate benchmark JSON data

## Setup & Running
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Testing
```bash
pytest
```
