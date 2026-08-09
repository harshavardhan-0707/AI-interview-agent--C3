import json
from typing import Dict, Any, List


SYSTEM_INTERVIEWER_PROMPT = """You are a senior principal AI engineer and technical interviewer conducting a live conversational interview for a technical candidate.

Target Candidate Profile:
- Name: {candidate_name}
- Job Role: {job_role}
- Experience: {experience_years} years ({difficulty} Level)
- Commit Activity: {commit_days} active commit days across cohort
- Topics to Cover: {topics_to_cover}
- Areas Needing Probe/Validation: {struggled_topics}

INTERVIEW RULES:
1. Conduct a professional, technical conversation. Ask ONE clear, focused question at a time.
2. Direct questions specifically to their experience level ({difficulty}) and their specific role ({job_role}).
3. If the candidate struggled with a topic (e.g. {struggled_topics}), formulate a targeted technical scenario to evaluate their real understanding.
4. Adapt difficulty: If the candidate gives a deep, accurate answer, increase technical depth or ask about edge cases/trade-offs. If they give a brief or weak answer, probe gently or guide them to core principles.
5. Do NOT repeat questions already asked. Maintain conversation context seamlessly.
6. Do NOT output generic lists of multiple questions. Ask exactly ONE question.
7. Keep responses concise, direct, and conversational.
"""


FEEDBACK_GENERATION_PROMPT = """You are an expert technical interviewer evaluating a completed technical interview.

Candidate Profile:
- Name: {candidate_name}
- Role: {job_role} ({experience_years} yrs exp)
- Difficulty Level: {difficulty}

Interview Transcript & Evaluations:
{transcript_text}

Generate structured evaluation feedback in strict JSON format:
{{
  "summary": "Concise 2-3 sentence overall evaluation summary of technical competence, communication, and performance.",
  "strengths": [
    "Specific technical strength demonstrated during interview",
    "Another demonstrated strength"
  ],
  "gaps": [
    "Identified skill gap or area needing improvement",
    "Another gap or missed nuance"
  ],
  "next": [
    "Actionable learning step or recommended project",
    "Another next step"
  ]
}}

Ensure every array has at least 2 concise, actionable points.
Return ONLY valid JSON.
"""


def build_system_prompt(analysis: Dict[str, Any]) -> str:
    return SYSTEM_INTERVIEWER_PROMPT.format(
        candidate_name=analysis["candidate_name"],
        job_role=analysis["job_role"],
        experience_years=analysis["experience_years"],
        difficulty=analysis["difficulty"],
        commit_days=analysis["commit_days"],
        topics_to_cover=", ".join(analysis["selected_topics"]),
        struggled_topics=", ".join(analysis["struggled_topics"]) if analysis["struggled_topics"] else "None (Strong performance across curriculum)"
    )


def build_feedback_prompt(analysis: Dict[str, Any], transcript: List[Dict[str, str]]) -> str:
    transcript_text = ""
    for entry in transcript:
        role = "Interviewer" if entry["role"] == "interviewer" else "Candidate"
        transcript_text += f"{role}: {entry['content']}\n\n"

    return FEEDBACK_GENERATION_PROMPT.format(
        candidate_name=analysis["candidate_name"],
        job_role=analysis["job_role"],
        experience_years=analysis["experience_years"],
        difficulty=analysis["difficulty"],
        transcript_text=transcript_text
    )
