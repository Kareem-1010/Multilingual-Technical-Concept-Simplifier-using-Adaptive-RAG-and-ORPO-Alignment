from fastapi import APIRouter, Depends
from feedback.store import get_history
from typing import List
from api.schemas import HistoryItem
from api.dependencies import get_current_user

router = APIRouter()

@router.get("/history", response_model=List[HistoryItem])
async def fetch_history(limit: int = 20, current_user: dict = Depends(get_current_user)):
    history = await get_history(user_id=current_user['id'], limit=limit)
    return history
