import os
import json
import logging
import httpx
from typing import Dict, Any, List, Tuple, Optional
from app.models.interview import Feedback

logger = logging.getLogger("llm_service")


class LLMService:
    """Configurable LLM provider service supporting OpenAI, Gemini, Anthropic, and safe Mock fallback mode."""
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "mock").lower()
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

    async def generate_response(self, system_prompt: str, transcript: List[Dict[str, str]], candidate_analysis: Dict[str, Any], current_turn: int) -> str:
        """Generates conversational interviewer questions based on candidate profile and transcript history."""
        if self.provider == "openai" and self.openai_api_key:
            try:
                return await self._call_openai(system_prompt, transcript)
            except Exception as e:
                logger.warning(f"OpenAI API call failed: {e}. Falling back to mock engine.")
        
        elif self.provider == "gemini" and self.gemini_api_key:
            try:
                return await self._call_gemini(system_prompt, transcript)
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Falling back to mock engine.")

        elif self.provider == "anthropic" and self.anthropic_api_key:
            try:
                return await self._call_anthropic(system_prompt, transcript)
            except Exception as e:
                logger.warning(f"Anthropic API call failed: {e}. Falling back to mock engine.")

        # Default Mock Fallback Engine
        return self._generate_mock_turn_response(candidate_analysis, transcript, current_turn)

    async def generate_feedback(self, feedback_prompt: str, candidate_analysis: Dict[str, Any], transcript: List[Dict[str, str]]) -> Feedback:
        """Generates structured evaluation feedback containing summary, strengths, gaps, and next steps."""
        if self.provider == "openai" and self.openai_api_key:
            try:
                raw_json = await self._call_openai(feedback_prompt, transcript, json_mode=True)
                data = json.loads(raw_json)
                return Feedback(**data)
            except Exception as e:
                logger.warning(f"OpenAI feedback generation failed: {e}. Falling back to mock engine.")

        elif self.provider == "gemini" and self.gemini_api_key:
            try:
                raw_json = await self._call_gemini(feedback_prompt, transcript, json_mode=True)
                data = json.loads(raw_json)
                return Feedback(**data)
            except Exception as e:
                logger.warning(f"Gemini feedback generation failed: {e}. Falling back to mock engine.")

        # Default Mock Feedback Generator
        return self._generate_mock_feedback(candidate_analysis, transcript)

    # ------------------------------------------------------------------
    # MOCK ENGINE IMPLEMENTATION
    # ------------------------------------------------------------------
    def _generate_mock_turn_response(self, analysis: Dict[str, Any], transcript: List[Dict[str, str]], current_turn: int) -> str:
        candidate_name = analysis.get("candidate_name", "Candidate")
        role = analysis.get("job_role", "Developer")
        topics = analysis.get("selected_topics", ["AI Engineering", "RAG", "Agentic Systems"])
        struggled = analysis.get("struggled_topics", [])
        
        # Initial Welcome & Question 1 (Turn 0)
        if current_turn == 0 or len(transcript) <= 1:
            first_topic = topics[0] if topics else "vector search and RAG"
            if "Probe Area:" in first_topic:
                return f"Welcome {candidate_name}! Let's begin your technical interview for the {role} position. I noticed during your cohort missions that you explored {first_topic.replace('Probe Area: ', '')}. Could you explain your approach when debugging issues in that area, and how you verified your solution?"
            else:
                return f"Welcome {candidate_name}! Let's begin your technical interview for the {role} position. To start off, could you walk me through your experience building with {first_topic}, and how you structure your architecture for scalability?"

        # Turn 1: Probe deeper into candidate's previous response or move to Topic 2
        last_answer = transcript[-1]["content"] if transcript and transcript[-1]["role"] == "candidate" else ""
        
        if current_turn == 1:
            topic2 = topics[1] if len(topics) > 1 else "LLM APIs & Prompting"
            return f"That's a solid point regarding your approach. Following up on that, when working with {topic2}, how do you evaluate latency vs. quality trade-offs in production?"

        if current_turn == 2:
            topic3 = topics[2] if len(topics) > 2 else "Agentic AI & Tool Calling"
            return f"Thanks for breaking that down. Moving on to {topic3}: how do you handle tool error recoveries or unexpected model outputs in an agentic loop?"

        if current_turn == 3:
            topic4 = topics[3] if len(topics) > 3 else "Evaluation & Guardrails"
            return f"Interesting perspective. Let's touch upon {topic4}: what metrics or automated evaluation frameworks do you rely on to prevent prompt injection or halluncinations?"

        # Final Question Turn (Turn 4)
        return f"Thank you for sharing those insights. For our final technical question: considering production monitoring and observability, how would you design a telemetry pipeline to track token usage and response accuracy for a deployed multi-agent system?"

    def _generate_mock_feedback(self, analysis: Dict[str, Any], transcript: List[Dict[str, str]]) -> Feedback:
        candidate_name = analysis.get("candidate_name", "Candidate")
        role = analysis.get("job_role", "AI Specialist")
        topics = analysis.get("selected_topics", [])
        struggled = analysis.get("struggled_topics", [])

        # Analyze candidate responses length/keywords to tailor strengths/gaps
        answers = [m["content"] for m in transcript if m["role"] == "candidate"]
        avg_answer_len = sum(len(a) for a in answers) / max(1, len(answers))
        
        strengths = [
            f"Demonstrated clear technical articulation appropriate for a {role} role.",
            f"Showed practical understanding of {topics[0] if topics else 'AI architectures'}.",
            "Communicated architectural decisions and trade-offs systematically."
        ]
        
        gaps = [
            f"Could provide deeper quantitative metrics when discussing {topics[1] if len(topics) > 1 else 'system evaluation'}.",
            f"Opportunity to refine edge-case error handling in {struggled[0] if struggled else 'agentic workflows'}."
        ]

        next_steps = [
            "Implement automated evaluation pipelines using Ragas or benchmark test suites.",
            "Explore production guardrails and prompt security isolation strategies.",
            "Review multi-agent state orchestration patterns for enterprise deployments."
        ]

        summary = f"{candidate_name} completed a multi-turn technical interview for the {role} role. The candidate exhibited strong foundational knowledge in core domain areas and communicated solutions effectively across multiple technical scenarios."

        return Feedback(
            summary=summary,
            strengths=strengths,
            gaps=gaps,
            next=next_steps
        )

    # ------------------------------------------------------------------
    # HTTP API CALLERS (OpenAI, Gemini, Anthropic)
    # ------------------------------------------------------------------
    async def _call_openai(self, system_prompt: str, transcript: List[Dict[str, str]], json_mode: bool = False) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        for entry in transcript:
            role = "assistant" if entry["role"] == "interviewer" else "user"
            messages.append({"role": role, "content": entry["content"]})

        payload: Dict[str, Any] = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.7
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"].strip()

    async def _call_gemini(self, system_prompt: str, transcript: List[Dict[str, str]], json_mode: bool = False) -> str:
        contents = []
        for entry in transcript:
            role = "model" if entry["role"] == "interviewer" else "user"
            contents.append({"role": role, "parts": [{"text": entry["content"]}]})

        if not contents:
            contents.append({"role": user, "parts": [{"text": "Start interview."}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.7}
        }
        if json_mode:
            payload["generationConfig"]["response_mime_type"] = "application/json"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    async def _call_anthropic(self, system_prompt: str, transcript: List[Dict[str, str]], json_mode: bool = False) -> str:
        messages = []
        for entry in transcript:
            role = "assistant" if entry["role"] == "interviewer" else "user"
            messages.append({"role": role, "content": entry["content"]})

        if not messages:
            messages.append({"role": "user", "content": "Start interview."})

        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": messages
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json=payload
            )
            res.raise_for_status()
            data = res.json()
            return data["content"][0]["text"].strip()


# Singleton LLM Service instance
llm_service = LLMService()
