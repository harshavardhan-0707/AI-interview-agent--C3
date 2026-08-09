import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes.interview import router as interview_router

load_dotenv()

app = FastAPI(
    title="AI Interview Agent API",
    description="Conversational technical interviewer personalized to candidate profile and curriculum history",
    version="1.0.0"
)

# Setup CORS middleware
origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(interview_router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AI Interview Agent API",
        "endpoint": "POST /api/interview"
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok", "provider": os.getenv("LLM_PROVIDER", "mock")}


@app.get("/api/candidates")
def get_sample_candidates():
    """Returns sample candidates from dataset for easy frontend testing."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "cohort_candidates.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            return data.get("sampleCandidates", [])
    return []
