# Prompt Log

## Prompt 1 - Project Setup & Architecture Plan
You are the senior full-stack engineer building my Hackathon project: AI Interview Agent.
Build an AI Interview Agent that conducts a conversational technical interview personalized to a candidate's profile and learning history.

- Mandatory API: POST /api/interview (sessionId state, reply, done, feedback)
- Personalization based on candidate profile, completed/failed/skipped missions, job role, and experience across an 8-module, 31-day curriculum cohort.
- Backend: Python + FastAPI
- Frontend: React + Vite + Tailwind CSS
- Robust LLM abstraction with mock fallback mode.
- Comprehensive session management, error handling, unit testing, and documentation.

---

## Prompt 2 - Full Implementation & Integration
- Approved Implementation Plan execution:
  1. Implemented cohort curriculum & sample candidates data in `backend/data/cohort_candidates.json`.
  2. Implemented candidate, request, response, and feedback Pydantic models in `backend/app/models/`.
  3. Implemented in-memory stateful `SessionManager` by `sessionId` in `backend/app/session/`.
  4. Implemented `PersonalizationService` mapping mission history, commit days, and job roles to focus topics and difficulty levels in `backend/app/services/`.
  5. Implemented `LLMService` with configurable providers (OpenAI, Gemini, Anthropic) and zero-dependency mock fallback engine in `backend/app/services/`.
  6. Implemented `InterviewEngine` and `POST /api/interview` FastAPI route in `backend/app/routes/`.
  7. Implemented backend Pytest test suite in `backend/tests/test_interview_api.py`.
  8. Implemented modern dark-mode React UI in `frontend/src/` with candidate selection modal, progress bar, conversational chat interface, and feedback summary dashboard.
