from typing import List, Optional, Any
from pydantic import BaseModel, Field
from app.models.candidate import CandidateProfile


class Feedback(BaseModel):
    summary: str = Field(..., description="Overall evaluation summary")
    strengths: List[str] = Field(default_factory=list, description="Key candidate strengths observed")
    gaps: List[str] = Field(default_factory=list, description="Technical skill gaps identified")
    next: List[str] = Field(default_factory=list, description="Actionable next learning steps")


class InterviewRequest(BaseModel):
    sessionId: str = Field(..., description="Unique interview session identifier")
    candidate: Optional[CandidateProfile] = Field(None, description="Candidate payload supplied on interview start")
    message: Optional[str] = Field(None, description="Candidate response message during conversation turn")


class InterviewResponse(BaseModel):
    reply: str = Field(..., description="Interviewer response or feedback notice")
    done: bool = Field(default=False, description="Whether the interview session has concluded")
    feedback: Optional[Feedback] = Field(None, description="Structured evaluation feedback when done=true")
