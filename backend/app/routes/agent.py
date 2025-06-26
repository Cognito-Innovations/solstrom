from fastapi import APIRouter, Request, HTTPException, Depends
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from app.utils.app_utils import get_app
from app.external_services.db import DB
from app.config import GOOGLE_CLIENT_ID
from app.utils.dependencies import get_db 

agent_router = APIRouter(prefix="/agent", tags=["agent_router"])

@agent_router.post("/auth/google")
async def auth_google(request: Request, db: DB = Depends(get_db)):
    """Handles Google login by verifying the token, and creating/retrieving the user."""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google Client ID is not configured on the server.")

    try:
        body = await request.json()
        token = body.get("token")
        if not token:
            raise HTTPException(status_code=400, detail="Token is missing.")

        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

        user_id = id_info.get("sub")
        email = id_info.get("email")
        name = id_info.get("name")

        if not all([user_id, email, name]):
             raise HTTPException(status_code=400, detail="Invalid token payload.")

        user = db.get_user(user_id)
        
        if user is None:
            user = db.create_user(user_id, email, name)

        msg_count = db.count_user_messages(user_id)
        
        return {
            "success": True,
            "user": {
                "id": user.get("user_id"),
                "email": user.get("email"),
                "name": user.get("name"),
            },
            "isPaid": user.get("paid", False),
            "isFree": user.get("free", True),
            "messageCount": msg_count
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid Google Token: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agent_router.post("/conversation")
async def agent_conversation(request: Request, db: DB = Depends(get_db)):
    body = await request.json()
    user_message = body["message"]
    user_info = body.get("user")

    app = get_app()

    if not user_info:
        conversation = await app.agent_service.conversation(user_message, db=db)
        return {"success": True, "conversation": conversation, "limitReached": False, "free": True}

    user_id = user_info.get("id")
    user = db.get_user(user_id)
    
    if user is None:
        email = user_info.get("email")
        name = user_info.get("name")
        user = db.create_user(user_id, email, name)

    free = user.get("free", True)
    paid = user.get("paid", False)

    msg_count = db.count_user_messages(user_id)

    if free and not paid and msg_count >= 5:
        return {
            "success": True,
            "conversation": {"response": ["You have reached your free message limit."]},
            "limitReached": True,
            "free": free,
            "paid": paid
        }

    conversation = await app.agent_service.conversation(user_message, db=db)
    db.store_message(user_id, user_message, str(conversation))

    limit_reached_after_send = free and not paid and (msg_count + 1) >= 5

    return {
        "success": True,
        "conversation": conversation,
        "limitReached": limit_reached_after_send,
        "free": free,
        "paid": paid
    }

@agent_router.post("/user/pay")
async def user_pay(request: Request, db: DB = Depends(get_db)):
    body = await request.json()
    user_id = body.get("userId")
    if not user_id:
        return {"success": False, "error": "Missing userId"}
    db.set_user_paid(user_id)
    return {"success": True}