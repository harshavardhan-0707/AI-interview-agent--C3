import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.session.session_manager import session_store

client = TestClient(app)

SAMPLE_CANDIDATE = {
    "id": "test-cand-001",
    "name": "Jordan Lee",
    "jobRole": "AI Engineer",
    "yearsExperience": 3.5,
    "education": "B.S. Computer Science",
    "status": "active",
    "completedMissions": ["m1_env_setup", "m7_embeddings_calc", "m8_vector_db_setup", "m17_tool_calling"],
    "failedMissions": ["m22_prompt_security"],
    "skippedMissions": ["m3_docker_basics"],
    "missionAttempts": {"m22_prompt_security": 3},
    "signals": {
        "commitDays": 20,
        "missionsCompleted": 10,
        "missionsFirstTry": 8
    }
}


def setup_function():
    # Clear session store before each test
    session_store._sessions.clear()


def test_start_interview_success():
    """Verify POST /api/interview initializes session and returns reply."""
    payload = {
        "sessionId": "session-test-01",
        "candidate": SAMPLE_CANDIDATE
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["done"] is False
    assert data["feedback"] is None
    assert len(data["reply"]) > 0
    # Verify session persisted
    assert session_store.session_exists("session-test-01")


def test_personalization_probing():
    """Verify candidate personalization engine targets failed mission topics."""
    payload = {
        "sessionId": "session-test-personalization",
        "candidate": SAMPLE_CANDIDATE
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 200
    session = session_store.get_session("session-test-personalization")
    assert session is not None
    # Failed mission m22_prompt_security mapped to prompt security topic
    struggled = session.analysis_data["struggled_topics"]
    assert len(struggled) > 0
    assert "security" in struggled[0].lower()


def test_continue_interview_turns():
    """Verify session continuation across multiple conversation turns."""
    session_id = "session-test-02"
    
    # 1. Start session
    client.post("/api/interview", json={"sessionId": session_id, "candidate": SAMPLE_CANDIDATE})
    
    # 2. First turn
    turn1_payload = {"sessionId": session_id, "message": "I prefer using Cosine distance when vectors are unit length."}
    res1 = client.post("/api/interview", json=turn1_payload)
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["done"] is False
    assert len(d1["reply"]) > 0

    # 3. Second turn
    turn2_payload = {"sessionId": session_id, "message": "We mitigate latency by leveraging HNSW index parameters."}
    res2 = client.post("/api/interview", json=turn2_payload)
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["done"] is False


def test_session_state_isolation():
    """Verify distinct session IDs maintain isolated state and transcripts."""
    s1 = "session-alpha"
    s2 = "session-beta"

    client.post("/api/interview", json={"sessionId": s1, "candidate": SAMPLE_CANDIDATE})
    client.post("/api/interview", json={"sessionId": s2, "candidate": {**SAMPLE_CANDIDATE, "name": "Taylor Swift"}})

    client.post("/api/interview", json={"sessionId": s1, "message": "Alpha answer 1"})

    session1 = session_store.get_session(s1)
    session2 = session_store.get_session(s2)

    assert session1.current_turn == 1
    assert session2.current_turn == 0
    assert session1.candidate.name == "Jordan Lee"
    assert session2.candidate.name == "Taylor Swift"


def test_interview_completion_and_feedback_structure():
    """Verify interview concludes and generates structured feedback after max turns."""
    session_id = "session-test-complete"
    
    # Start session
    client.post("/api/interview", json={"sessionId": session_id, "candidate": SAMPLE_CANDIDATE})
    
    # Send 5 turns to complete max turns
    for i in range(5):
        msg = f"Candidate response turn {i+1} covering technical details."
        res = client.post("/api/interview", json={"sessionId": session_id, "message": msg})
        assert res.status_code == 200
        data = res.json()
        if i < 4:
            assert data["done"] is False
        else:
            # 5th turn should conclude interview
            assert data["done"] is True
            assert "reply" in data
            assert data["feedback"] is not None
            
            fb = data["feedback"]
            assert "summary" in fb and isinstance(fb["summary"], str)
            assert "strengths" in fb and isinstance(fb["strengths"], list) and len(fb["strengths"]) >= 1
            assert "gaps" in fb and isinstance(fb["gaps"], list) and len(fb["gaps"]) >= 1
            assert "next" in fb and isinstance(fb["next"], list) and len(fb["next"]) >= 1


def test_get_sample_candidates_endpoint():
    """Verify GET /api/candidates endpoint returns cohort benchmark data."""
    res = client.get("/api/candidates")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_invalid_request_handling():
    """Verify error handling for missing fields, invalid candidate data, and unknown session."""
    # Missing sessionId
    res1 = client.post("/api/interview", json={"candidate": SAMPLE_CANDIDATE})
    assert res1.status_code == 422 or res1.status_code == 400

    # Unknown session ID turn
    res2 = client.post("/api/interview", json={"sessionId": "unknown-session-xyz", "message": "hello"})
    assert res2.status_code == 404

    # Empty payload
    res3 = client.post("/api/interview", json={"sessionId": "test-session"})
    assert res3.status_code == 400
