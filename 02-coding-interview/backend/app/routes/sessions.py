from fastapi import APIRouter, HTTPException, status, Depends, Query
from ..schemas import (
    SessionCreate, SessionUpdate, Session, SessionDetail, 
    ExecutionRequest, ExecutionResult, Participant, SessionList, Language
)
from ..database import db
from ..security import verify_token
from ..executor import CodeExecutor

router = APIRouter()

@router.post("", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate, user_id: str = Depends(verify_token)):
    """Create a new interview session"""
    session = db.create_session(
        title=session_data.title,
        language=session_data.language,
        created_by=user_id,
        description=session_data.description
    )
    return session

@router.get("", response_model=SessionList)
async def get_sessions(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: str = Depends(verify_token)
):
    """Get all sessions for current user"""
    sessions, total = db.get_user_sessions(user_id, limit, offset)
    return SessionList(total=total, items=sessions)

@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(session_id: str):
    """Get session details"""
    session_data = db.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    participants = db.get_participants(session_id)
    
    return SessionDetail(
        id=session_data["id"],
        title=session_data["title"],
        language=Language(session_data["language"]),
        code=session_data.get("code", ""),
        description=session_data.get("description", ""),
        created_by=session_data["created_by"],
        created_at=session_data["created_at"],
        updated_at=session_data["updated_at"],
        participant_count=len(participants),
        participants=participants
    )

@router.put("/{session_id}", response_model=SessionDetail)
async def update_session(
    session_id: str,
    session_update: SessionUpdate,
    user_id: str = Depends(verify_token)
):
    """Update session (creator only)"""
    session_data = db.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session_data["created_by"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only session creator can update"
        )
    
    update_dict = session_update.model_dump(exclude_unset=True)
    if "language" in update_dict and isinstance(update_dict["language"], Language):
        update_dict["language"] = update_dict["language"].value
    
    updated_session = db.update_session(session_id, **update_dict)
    
    participants = db.get_participants(session_id)
    
    return SessionDetail(
        id=updated_session["id"],
        title=updated_session["title"],
        language=Language(updated_session["language"]),
        code=updated_session.get("code", ""),
        description=updated_session.get("description", ""),
        created_by=updated_session["created_by"],
        created_at=updated_session["created_at"],
        updated_at=updated_session["updated_at"],
        participant_count=len(participants),
        participants=participants
    )

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, user_id: str = Depends(verify_token)):
    """Delete session (creator only)"""
    session_data = db.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session_data["created_by"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only session creator can delete"
        )
    
    db.delete_session(session_id)
    return None

@router.post("/{session_id}/execute", response_model=ExecutionResult)
async def execute_code(session_id: str, execution: ExecutionRequest):
    """Execute code in session"""
    session_data = db.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    result = await CodeExecutor.execute(execution.code, execution.language, execution.input)
    return result

@router.get("/{session_id}/participants", response_model=list[Participant])
async def get_participants(session_id: str):
    """Get session participants"""
    session_data = db.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return db.get_participants(session_id)
