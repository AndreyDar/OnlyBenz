from fastapi import APIRouter
from ..api.chat_api import get_chat_client_response

router = APIRouter()

@router.get("/chat-client-messages/")
async def chat_client_messages():
    return await get_chat_client_response()