from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"


class User(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {"from_attributes": True}


class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user: User
    access_token: str
    token_type: str


class HealthResponse(BaseModel):
    status: str
    timestamp: Optional[datetime] = None


class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    language: Language = Language.PYTHON
    time_limit_minutes: int = Field(default=60, ge=1, le=480)


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Participant(BaseModel):
    user_id: str
    username: str
    joined_at: datetime


class ExecutionRequest(BaseModel):
    code: str
    language: Language = Language.PYTHON
    stdin: Optional[str] = None


class ExecutionResult(BaseModel):
    success: bool = True
    output: str = ""
    stdout: str = ""
    stderr: str = ""
    return_code: int = 0
    execution_time: float = 0


class Session(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_by: str
    language: Language
    created_at: datetime
    time_limit_minutes: int
    participant_count: Optional[int] = 0
    
    model_config = {"from_attributes": True}


class SessionDetail(Session):
    participants: List[Participant] = []
    code: Optional[str] = None
    last_execution: Optional[ExecutionResult] = None


class SessionList(BaseModel):
    sessions: List[Session]
    total: int
