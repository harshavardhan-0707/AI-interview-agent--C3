import json
import os
from typing import List, Dict, Any, Tuple
from app.models.candidate import CandidateProfile

# Mission to Module Mapping & Topic Keywords
MISSION_TOPIC_MAP = {
    "m1_env_setup": ("Environment & Tooling", "Python environments and Docker containerization"),
    "m2_git_workflow": ("Environment & Tooling", "Git branching and team workflow"),
    "m3_docker_basics": ("Environment & Tooling", "Docker container optimization"),
    "m4_pandas_wrangling": ("Data Foundations", "Pandas data wrangling and transformation"),
    "m5_data_cleaning": ("Data Foundations", "Data validation and cleaning pipelines"),
    "m6_json_parsing": ("Data Foundations", "Structured JSON parsing and schema validation"),
    "m7_embeddings_calc": ("Embeddings & Vector Search", "Vector embeddings and cosine distance metrics"),
    "m8_vector_db_setup": ("Embeddings & Vector Search", "Vector database indexing (HNSW/IVF) and retrieval"),
    "m9_rag_retrieval_basic": ("Embeddings & Vector Search", "Retrieval-Augmented Generation (RAG) architecture"),
    "m10_prompt_crafting": ("LLM Core & Prompting", "Prompt engineering techniques and Chain-of-Thought"),
    "m11_llm_api_integration": ("LLM Core & Prompting", "LLM API integration and rate limiting"),
    "m12_cot_reasoning": ("LLM Core & Prompting", "Chain-of-thought and structured reasoning outputs"),
    "m13_finetuning_prep": ("LLM Core & Prompting", "LoRA and fine-tuning dataset preparation"),
    "m14_fastapi_backend": ("Chatbot Application Build", "FastAPI async backend architecture"),
    "m15_chat_history_state": ("Chatbot Application Build", "Stateful chat history and context window management"),
    "m16_streaming_ui": ("Chatbot Application Build", "Server-Sent Events and response streaming"),
    "m17_tool_calling": ("Agentic AI & MCP", "Function calling and tool integration"),
    "m18_react_agent": ("Agentic AI & MCP", "ReAct agent loops and reasoning step execution"),
    "m19_mcp_server": ("Agentic AI & MCP", "Model Context Protocol (MCP) server & client architecture"),
    "m20_multi_agent_system": ("Agentic AI & MCP", "Multi-agent coordination and orchestration"),
    "m21_ragas_eval": ("Evaluation & Security", "RAG evaluation metrics (Ragas, Faithfulness, Answer Relevance)"),
    "m22_prompt_security": ("Evaluation & Security", "Prompt injection security and guardrails"),
    "m23_docker_cloud_deploy": ("Evaluation & Security", "Cloud container deployment and scalability"),
    "m24_observability_setup": ("Production & Capstone", "LLM observability, telemetry, and tracing"),
    "m25_capstone_project": ("Production & Capstone", "End-to-end production AI system design")
}


class PersonalizationService:
    """Analyzes candidate profiles, cohort curriculum history, and signals to personalize technical interview plans."""
    
    @staticmethod
    def analyze_candidate(candidate: CandidateProfile) -> Dict[str, Any]:
        # 1. Identify Struggled / Failed Mission Topics (High Priority probes)
        struggled_topics = []
        for m_id in candidate.failedMissions:
            if m_id in MISSION_TOPIC_MAP:
                module, topic = MISSION_TOPIC_MAP[m_id]
                struggled_topics.append(f"{topic} (Module: {module})")
        
        # Check high attempt counts (>1 attempt)
        for m_id, attempts in candidate.missionAttempts.items():
            if attempts > 1 and m_id in MISSION_TOPIC_MAP:
                module, topic = MISSION_TOPIC_MAP[m_id]
                topic_desc = f"{topic} (Module: {module})"
                if topic_desc not in struggled_topics:
                    struggled_topics.append(topic_desc)

        # 2. Identify Mastered / Completed Mission Topics
        mastered_topics = []
        for m_id in candidate.completedMissions:
            if m_id in MISSION_TOPIC_MAP:
                module, topic = MISSION_TOPIC_MAP[m_id]
                mastered_topics.append(f"{topic} (Module: {module})")

        # 3. Determine Candidate Level & Role Focus
        role = candidate.jobRole.lower()
        exp = candidate.yearsExperience
        
        role_focus = []
        if "ai" in role or "machine learning" in role or "llm" in role:
            role_focus = ["Embeddings & Vector Search", "Agentic AI & MCP", "LLM Core & Prompting", "RAG Evaluation & Guardrails"]
        elif "data" in role or "scientist" in role or "analytics" in role:
            role_focus = ["Data Foundations", "Embeddings & Vector Search", "RAG Evaluation & Metrics", "LLM Fine-Tuning"]
        elif "full" in role or "software" in role or "backend" in role or "frontend" in role:
            role_focus = ["Chatbot Application Build", "FastAPI & Streaming", "Agentic AI & Tool Calling", "System Architecture"]
        else:
            role_focus = ["LLM Application Architecture", "Embeddings & Vector Search", "Agentic Workflows"]

        # 4. Generate Select List of 5 Focus Topics for the Interview
        selected_topics = []
        
        # Priority A: Address struggled topic if any
        if struggled_topics:
            selected_topics.append(f"Probe Area: {struggled_topics[0]}")

        # Priority B: Deep questions in primary role focus areas
        for focus in role_focus:
            if len(selected_topics) < 4:
                selected_topics.append(focus)
                
        # Priority C: Production / Security capstone validation
        if len(selected_topics) < 5:
            selected_topics.append("Production Observability & Guardrails")

        # 5. Determine Difficulty Level
        first_try_rate = (candidate.signals.missionsFirstTry / max(1, candidate.signals.missionsCompleted))
        if exp >= 4 or (first_try_rate > 0.8 and candidate.signals.commitDays > 20):
            difficulty = "Senior / Advanced"
        elif exp >= 2 or candidate.signals.commitDays > 10:
            difficulty = "Mid-Level / Intermediate"
        else:
            difficulty = "Junior / Foundational"

        return {
            "candidate_name": candidate.name,
            "job_role": candidate.jobRole,
            "experience_years": candidate.yearsExperience,
            "difficulty": difficulty,
            "struggled_topics": struggled_topics,
            "mastered_topics": mastered_topics,
            "selected_topics": selected_topics,
            "commit_days": candidate.signals.commitDays,
            "missions_completed": len(candidate.completedMissions)
        }
