# AI Interview Agent 🚀

An intelligent, conversational technical interviewer personalized to a candidate's background, job role, experience level, and learning history across a 31-day curriculum cohort.

---

## 📌 Problem Statement
Traditional technical interviews often use static, generic question lists that fail to adapt to a candidate's specific background, hands-on experience, or learning history. Evaluating candidates accurately requires dynamic, context-aware probing into their actual completed projects, failed topics, and domain strengths.

## 💡 Solution
The **AI Interview Agent** delivers dynamic, multi-turn technical interviews tailored to each candidate. By ingesting candidate performance data—such as completed, failed, and skipped missions, commit activity, and experience level—the agent generates targeted questions, probes candidate responses, dynamically adjusts difficulty, and delivers structured feedback summaries upon completion.

---

## ✨ Features
- **Candidate Personalization Engine**: Analyzes candidate roles, experience, commit history, and mission history (completed/failed/skipped) to tailor question topics.
- **Conversational Multi-Turn State**: Maintains session context across multiple turns via `sessionId`.
- **Adaptive Probing**: Evaluates responses in real-time, asking relevant follow-up questions or transitioning topics seamlessly.
- **Configurable LLM Abstraction**: Supports Gemini, OpenAI, Anthropic, and a zero-dependency **Mock Engine** for robust offline development.
- **Structured Feedback Dashboard**: Generates end-of-interview feedback containing actionable summaries, key strengths, skill gaps, and recommended next steps.
- **Modern UI**: Clean, dark-mode React interface with live messaging, progress indicators, typing states, and rich summary dashboards.

---

## 🛠️ Architecture & Tech Stack

```
[ Frontend: React + Vite + Tailwind CSS ]
                   │
         POST /api/interview
                   │
  [ Backend: FastAPI (Python 3.10+) ]
   ├── Session Store (In-Memory / Redis Ready)
   ├── Personalization Engine
   └── LLM Provider Service (Mock / OpenAI / Gemini / Anthropic)
```

- **Backend**: Python 3.10+, FastAPI, Pydantic, Uvicorn, Pytest
- **Frontend**: JavaScript/React, Vite, Tailwind CSS, Lucide Icons
- **LLM Integrations**: Google Gemini API, OpenAI API, Anthropic API, Custom Fallback Mock Engine

---

## 📁 Folder Structure

```
AI-interview-agent--C3/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── session/
│   │   └── utils/
│   ├── data/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── docs/
├── README.md
├── PROMPTS.md
├── .env.example
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Available configurations:
- `LLM_PROVIDER`: `mock` (default, no API key needed), `openai`, `gemini`, or `anthropic`.
- `OPENAI_API_KEY`: Required if provider is set to `openai`.
- `GEMINI_API_KEY`: Required if provider is set to `gemini`.
- `ANTHROPIC_API_KEY`: Required if provider is set to `anthropic`.

---

## 🚀 Running the Application

### 1. Backend Setup & Startup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend will run at: `http://localhost:8000`

### 2. Frontend Setup & Startup
```bash
cd frontend
npm install
npm run dev
```
Frontend will run at: `http://localhost:5173`

---

## 📡 API Specification

### Endpoint: `POST /api/interview`

#### 1. Start Interview
**Request:**
```json
{
  "sessionId": "session-123",
  "candidate": {
    "id": "cand-001",
    "name": "Jane Doe",
    "jobRole": "AI Engineer",
    "yearsExperience": 3,
    "education": "B.S. Computer Science",
    "completedMissions": ["m1", "m2", "m3"],
    "failedMissions": ["m4"],
    "skippedMissions": [],
    "signals": {
      "commitDays": 25,
      "missionsCompleted": 18,
      "missionsFirstTry": 15
    }
  }
}
```

**Response:**
```json
{
  "reply": "Welcome Jane Doe. Let's begin your technical interview. I noticed your experience with RAG and Embeddings—could you explain how you select distance metrics for vector indices?",
  "done": false
}
```

#### 2. Conversation Turn
**Request:**
```json
{
  "sessionId": "session-123",
  "message": "Cosine distance works well when vectors are normalized, whereas Euclidean distance measures spatial distance..."
}
```

**Response:**
```json
{
  "reply": "Great explanation. How do you handle dimensional indexing trade-offs when scaling HNSW parameters in production?",
  "done": false
}
```

#### 3. Interview Completion
**Response:**
```json
{
  "reply": "Thank you! That completes our technical interview session.",
  "done": true,
  "feedback": {
    "summary": "Jane demonstrated strong understanding of vector retrieval and indexing trade-offs, with solid architectural intuition.",
    "strengths": [
      "Deep grasp of vector similarity metrics (Cosine vs. Euclidean)",
      "Clear articulation of HNSW trade-offs in production"
    ],
    "gaps": [
      "Could elaborate more on fine-tuning strategies for cross-encoders"
    ],
    "next": [
      "Review advanced re-ranking techniques and hybrid BM25 + dense search implementations"
    ]
  }
}
```

---

## 🧪 Testing

Run backend test suite:
```bash
cd backend
pytest
```

---

## 📦 Deployment Instructions

1. **Backend Deployment**: Deploy the FastAPI app using Docker or Uvicorn on Cloud Run, Render, or AWS ECS.
2. **Frontend Deployment**: Build production bundle (`npm run build`) and host on Vercel, Netlify, or Firebase Hosting.
