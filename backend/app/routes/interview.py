from fastapi import APIRouter, HTTPException, status
from app.models.interview import InterviewRequest, InterviewResponse
from app.services.interview_engine import InterviewEngine
from app.session.session_manager import session_store

router = APIRouter()


@router.post("/interview", response_model=InterviewResponse)
async def handle_interview(req: InterviewRequest):
    """
    Mandatory AI Interview Endpoint.
    Handles both interview initialization (when candidate object is supplied) 
    and conversation turns (when message string is supplied).
    """
    # 1. Validate sessionId presence
    if not req.sessionId or not req.sessionId.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sessionId is required and cannot be empty."
        )

    session_id = req.sessionId.strip()
    session_exists = session_store.session_exists(session_id)

    # 2. Case A: Start Interview Request (Candidate payload provided)
    if req.candidate is not None:
        try:
            return await InterviewEngine.start_interview(session_id=session_id, candidate=req.candidate)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize interview session: {str(e)}"
            )

    # 3. Case B: Conversation Turn Request (Message payload provided)
    elif req.message is not None:
        if not session_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{session_id}' not found. Please start an interview first by providing candidate details."
            )

        if not req.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="message cannot be empty."
            )

        try:
            return await InterviewEngine.process_turn(session_id=session_id, message=req.message.strip())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process conversation turn: {str(e)}"
            )

    # 4. Invalid Request Payload
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request payload. Must provide either 'candidate' to start an interview or 'message' to continue an ongoing session."
        )
