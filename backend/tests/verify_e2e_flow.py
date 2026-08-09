import httpx
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_e2e_verification():
    print("=== Starting E2E HTTP Verification ===")
    
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Health check
        res = client.get("/api/health")
        print(f"Health Check: {res.status_code} -> {res.json()}")
        assert res.status_code == 200

        # 2. Get sample candidates
        res = client.get("/api/candidates")
        candidates = res.json()
        print(f"Loaded Candidates: {len(candidates)} candidates found.")
        assert len(candidates) > 0
        candidate = candidates[0]

        # 3. Start Interview
        session_id = f"e2e-session-{httpx.__name__}"
        start_payload = {
            "sessionId": session_id,
            "candidate": candidate
        }
        res = client.post("/api/interview", json=start_payload)
        print(f"Start Interview Response: {res.status_code}")
        start_data = res.json()
        print(f"Interviewer Reply 0: {start_data['reply']}")
        assert res.status_code == 200
        assert start_data["done"] is False
        assert len(start_data["reply"]) > 0

        # 4. Multi-turn conversation
        answers = [
            "I have 5 years of experience building vector search with ChromaDB and HNSW indexing.",
            "We evaluate RAG faithfulness using Ragas metrics and automated LLM-as-a-judge pipelines.",
            "For agentic tool calling, we use Pydantic schema validation and fallback error retry loops.",
            "To secure prompts against injection, we sanitize inputs and isolate system instructions.",
            "In production, we emit telemetry metrics to LangSmith and track p99 latency."
        ]

        for idx, answer in enumerate(answers):
            turn_payload = {
                "sessionId": session_id,
                "message": answer
            }
            res = client.post("/api/interview", json=turn_payload)
            assert res.status_code == 200
            data = res.json()
            print(f"Turn {idx+1} Response: done={data['done']}, reply_len={len(data['reply'])}")
            
            if idx < 4:
                assert data["done"] is False
            else:
                assert data["done"] is True
                assert "feedback" in data and data["feedback"] is not None
                fb = data["feedback"]
                print("\n=== FINAL FEEDBACK RECEIVED ===")
                print(f"Summary: {fb['summary']}")
                print(f"Strengths: {fb['strengths']}")
                print(f"Gaps: {fb['gaps']}")
                print(f"Next Steps: {fb['next']}")
                
                assert isinstance(fb["summary"], str) and len(fb["summary"]) > 0
                assert isinstance(fb["strengths"], list) and len(fb["strengths"]) >= 2
                assert isinstance(fb["gaps"], list) and len(fb["gaps"]) >= 2
                assert isinstance(fb["next"], list) and len(fb["next"]) >= 2

    print("\n✅ E2E HTTP Verification PASSED completely!")

if __name__ == "__main__":
    run_e2e_verification()
