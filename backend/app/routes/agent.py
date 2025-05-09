from fastapi import APIRouter, Request

from app.utils.app_utils import get_app

agent_router = APIRouter(prefix="/agent", tags=["agent_router"])

@agent_router.post("/conversation")
async def agent_conversation(request: Request):
    body = await request.json()
    user_message = body["message"]

    app = get_app()

    conversation = await app.agent_service.conversation(user_message)
    return {"success": True, "conversation": conversation}