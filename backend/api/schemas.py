from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SimplifyRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    target_language: str = Field(default="en")
    domain_hint: Optional[str] = None  # optional override
    session_id: Optional[str] = None

class SimplificationOutput(BaseModel):
    explanation: str
    key_terms: List[dict]  # [{term, definition}]
    analogy: str
    summary: str

class SimplifyResponse(BaseModel):
    query: str
    detected_language: str
    target_language: str
    domain: str
    domain_confidence: float
    output: SimplificationOutput
    faithfulness: dict       # {score, is_faithful, label}
    metrics: dict            # {readability_score, token_count, ...}
    retrieved_passages: List[str]
    processing_time_ms: int

class FeedbackRequest(BaseModel):
    session_id: str
    query: str
    domain: str
    language: str
    explanation: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    faithfulness_score: Optional[float] = None
    readability_score: Optional[float] = None

class HistoryItem(BaseModel):
    id: int
    query: str
    domain: str
    language: str
    rating: Optional[int]
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    
class UserInDB(UserResponse):
    hashed_password: str
