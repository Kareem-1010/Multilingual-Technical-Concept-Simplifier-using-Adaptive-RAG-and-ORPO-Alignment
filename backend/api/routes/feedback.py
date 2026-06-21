from fastapi import APIRouter, Depends
from api.schemas import FeedbackRequest
from feedback.store import insert_feedback
from api.dependencies import get_current_user

router = APIRouter()

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    data = request.model_dump()
    data['user_id'] = current_user['id']
    await insert_feedback(data)
    return {"status": "success", "message": "Feedback recorded."}
