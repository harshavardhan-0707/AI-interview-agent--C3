import logging
from typing import Dict, Any, Tuple
from app.models.candidate import CandidateProfile
from app.models.interview import InterviewResponse, Feedback
from app.session.session_manager import session_store, InterviewSession
from app.services.personalization_service import PersonalizationService
from app.services.llm_service import llm_service
from app.prompts.interviewer_prompts import build_system_prompt, build_feedback_prompt

logger = logging.getLogger("interview_engine")


class InterviewEngine:
    """Core logic orchestrating candidate personalization, stateful conversation turns, and feedback generation."""

    @staticmethod
    async def start_interview(session_id: str, candidate: CandidateProfile) -> InterviewResponse:
        # 1. Analyze candidate profile against cohort curriculum & signals
        analysis = PersonalizationService.analyze_candidate(candidate)
        
        # 2. Create and store new interview session
        session = session_store.create_session(
            session_id=session_id,
            candidate=candidate,
            topics=analysis["selected_topics"]
        )
        
        # Attach personalization analysis metadata to session
        session.analysis_data = analysis
        session.system_prompt = build_system_prompt(analysis)

        # 3. Generate initial question (Turn 0)
        initial_reply = await llm_service.generate_response(
            system_prompt=session.system_prompt,
            transcript=session.transcript,
            candidate_analysis=analysis,
            current_turn=0
        )

        # Record interviewer question in session transcript
        session.add_message(role="interviewer", content=initial_reply)
        
        return InterviewResponse(
            reply=initial_reply,
            done=False
        )

    @staticmethod
    async def process_turn(session_id: str, message: str) -> InterviewResponse:
        session = session_store.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found or expired.")

        if session.done:
            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=session.feedback
            )

        # 1. Record candidate answer in transcript
        session.add_message(role="candidate", content=message)
        session.record_turn(
            question=session.transcript[-2]["content"] if len(session.transcript) >= 2 else "",
            answer=message
        )

        # 2. Check if maximum interview turns reached (e.g. 5 questions completed)
        if session.current_turn >= session.max_turns:
            # Conclude interview & generate feedback
            feedback_prompt = build_feedback_prompt(session.analysis_data, session.transcript)
            feedback = await llm_service.generate_feedback(
                feedback_prompt=feedback_prompt,
                candidate_analysis=session.analysis_data,
                transcript=session.transcript
            )
            
            session.done = True
            session.feedback = feedback
            session.add_message(role="interviewer", content="Interview completed.")

            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=feedback
            )

        # 3. Generate next conversational interviewer question
        next_reply = await llm_service.generate_response(
            system_prompt=session.system_prompt,
            transcript=session.transcript,
            candidate_analysis=session.analysis_data,
            current_turn=session.current_turn
        )

        # Record interviewer reply in transcript
        session.add_message(role="interviewer", content=next_reply)

        return InterviewResponse(
            reply=next_reply,
            done=False
        )
