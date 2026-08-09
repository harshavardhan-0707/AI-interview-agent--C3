from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class CandidateSignals(BaseModel):
    commitDays: int = Field(default=0, description="Total days with active commits")
    missionsCompleted: int = Field(default=0, description="Total missions completed")
    missionsFirstTry: int = Field(default=0, description="Missions passed on the first attempt")


class CandidateProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(default="cand-default", description="Unique Candidate or Member ID")
    name: str = Field(..., description="Full Name of Candidate")
    jobRole: str = Field(default="AI Developer", description="Target or current job role")
    yearsExperience: float = Field(default=1.0, description="Years of professional experience")
    education: Optional[str] = Field(default="B.S. Computer Science", description="Educational background")
    status: Optional[str] = Field(default="active", description="Candidate cohort status")
    
    completedMissions: List[str] = Field(default_factory=list, description="List of completed mission IDs")
    failedMissions: List[str] = Field(default_factory=list, description="List of failed mission IDs")
    skippedMissions: List[str] = Field(default_factory=list, description="List of skipped mission IDs")
    
    missionAttempts: Dict[str, int] = Field(default_factory=dict, description="Attempts count per mission ID")
    signals: CandidateSignals = Field(default_factory=CandidateSignals, description="Performance signals")
