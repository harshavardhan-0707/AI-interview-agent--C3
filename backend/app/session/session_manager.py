import time
from typing import Dict, Optional, List, Any
from app.models.candidate import CandidateProfile
from app.models.interview import Feedback


class InterviewSession:
    def __init__(self, session_id: str, candidate: CandidateProfile, topics: List[str]):
        self.session_id: str = session_id
        self.candidate: CandidateProfile = candidate
        self.transcript: List[Dict[str, str]] = []
        self.current_turn: int = 0
        self.max_turns: int = 5  # 5 targeted questions per interview session
        self.topics_to_cover: List[str] = topics
        self.topics_covered: List[str] = []
        self.evaluations: List[Dict[str, Any]] = []
        self.done: bool = False
        self.feedback: Optional[Feedback] = None
        self.created_at: float = time.time()
        self.updated_at: float = time.time()

    def add_message(self, role: str, content: str):
        self.transcript.append({"role": role, "content": content})
        self.updated_at = time.time()

    def record_turn(self, question: str, answer: str, analysis: Optional[str] = None):
        self.evaluations.append({
            "turn": self.current_turn,
            "question": question,
            "answer": answer,
            "analysis": analysis
        })
        self.current_turn += 1
        self.updated_at = time.time()


class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, InterviewSession] = {}

    def create_session(self, session_id: str, candidate: CandidateProfile, topics: List[str]) -> InterviewSession:
        session = InterviewSession(session_id, candidate, topics)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        return session_id in self._sessions


# Global singleton instance for in-memory session management
session_store = SessionManager()
